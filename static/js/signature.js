/**
 * Jankalyaan Blood Bank System - E-Signature Controller (Donor Consent & Medical Officer)
 */

let canvas = null;
let ctx = null;
let isDrawing = false;
let hasSignature = false;

let donorCanvas = null;
let donorCtx = null;
let isDonorDrawing = false;
let hasDonorSignature = false;

let moSigMode = 'draw'; // 'draw' or 'stored'
let storedMoSignatureData = null;

function initSignaturePad() {
  // Medical Officer Canvas
  canvas = document.getElementById('signatureCanvas');
  if (canvas) {
    ctx = canvas.getContext('2d');
    resizeCanvas(canvas, ctx);

    canvas.addEventListener('pointerdown', (e) => startDrawing(e, ctx));
    canvas.addEventListener('pointermove', (e) => draw(e, ctx, (val) => hasSignature = val));
    canvas.addEventListener('pointerup', stopDrawing);
    canvas.addEventListener('pointercancel', stopDrawing);
    canvas.addEventListener('mouseleave', stopDrawing);
  }

  // Donor Consent Canvas
  donorCanvas = document.getElementById('donorSignatureCanvas');
  if (donorCanvas) {
    donorCtx = donorCanvas.getContext('2d');
    resizeCanvas(donorCanvas, donorCtx);

    donorCanvas.addEventListener('pointerdown', (e) => startDrawing(e, donorCtx));
    donorCanvas.addEventListener('pointermove', (e) => draw(e, donorCtx, (val) => hasDonorSignature = val));
    donorCanvas.addEventListener('pointerup', stopDrawing);
    donorCanvas.addEventListener('pointercancel', stopDrawing);
    donorCanvas.addEventListener('mouseleave', stopDrawing);
  }

  // Check currentUser pre-stored signature
  if (currentUser && currentUser.signature_data) {
    storedMoSignatureData = currentUser.signature_data;
    const previewBox = document.getElementById('storedSigPreview');
    if (previewBox) {
      previewBox.innerHTML = `<img src="${storedMoSignatureData}" style="max-height:80px; max-width:180px; object-fit:contain;" alt="Stored Signature">`;
    }
  }

  window.addEventListener('resize', () => {
    if (canvas && ctx) resizeCanvas(canvas, ctx);
    if (donorCanvas && donorCtx) resizeCanvas(donorCanvas, donorCtx);
  });
}

function resizeCanvas(c, cx) {
  if (!c || !cx) return;
  const rect = c.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  c.width = rect.width * dpr;
  c.height = rect.height * dpr;
  cx.scale(dpr, dpr);

  cx.strokeStyle = '#0F172A';
  cx.lineWidth = 2.5;
  cx.lineCap = 'round';
  cx.lineJoin = 'round';
}

function getPointerPos(c, evt) {
  const rect = c.getBoundingClientRect();
  return {
    x: evt.clientX - rect.left,
    y: evt.clientY - rect.top
  };
}

function startDrawing(evt, cx) {
  evt.preventDefault();
  isDrawing = true;
  const pos = getPointerPos(cx.canvas, evt);
  cx.beginPath();
  cx.moveTo(pos.x, pos.y);
}

function draw(evt, cx, setFlag) {
  if (!isDrawing) return;
  evt.preventDefault();
  const pos = getPointerPos(cx.canvas, evt);
  cx.lineTo(pos.x, pos.y);
  cx.stroke();
  if (setFlag) setFlag(true);
}

function stopDrawing() {
  isDrawing = false;
}

function clearSignature() {
  if (!canvas || !ctx) return;
  const rect = canvas.getBoundingClientRect();
  ctx.clearRect(0, 0, rect.width, rect.height);
  hasSignature = false;
}

function clearDonorSignature() {
  if (!donorCanvas || !donorCtx) return;
  const rect = donorCanvas.getBoundingClientRect();
  donorCtx.clearRect(0, 0, rect.width, rect.height);
  hasDonorSignature = false;
}

function toggleMoSigMode(mode) {
  moSigMode = mode;
  const storedBox = document.getElementById('storedSigContainer');
  const drawBox = document.getElementById('drawSigContainer');

  if (mode === 'stored') {
    if (!storedMoSignatureData) {
      showToast('No pre-stored digital signature found in your Profile. Please upload one in your Profile page or draw on canvas.', 'error');
      document.getElementById('choice_draw').checked = true;
      toggleMoSigMode('draw');
      return;
    }
    storedBox?.classList.remove('hidden');
    drawBox?.classList.add('hidden');
  } else {
    storedBox?.classList.add('hidden');
    drawBox?.classList.remove('hidden');
  }
}

async function confirmAndFinaliseRecord() {
  let moSigData = null;

  if (moSigMode === 'stored') {
    moSigData = storedMoSignatureData;
  } else {
    if (!hasSignature) {
      showToast('Please provide a Medical Officer signature before finalising.', 'error');
      return;
    }
    moSigData = canvas.toDataURL('image/png');
  }

  if (!moSigData) {
    showToast('Medical Officer signature is required.', 'error');
    return;
  }

  // Get Donor Consent Signature if drawn
  let donorSigData = hasDonorSignature && donorCanvas ? donorCanvas.toDataURL('image/png') : '';
  
  // Attach donor signature to consent before final saving
  const payloadData = getFormData();
  payloadData.consent.donor_signature_data = donorSigData;

  if (!currentRecordId) {
    const saved = await saveRecord(true);
    if (!saved) return;
  }

  const medicalNotes = document.getElementById('medical_notes')?.value || '';

  try {
    const res = await fetch(`/api/records/${currentRecordId}/sign`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        signature_data: moSigData,
        medical_notes: medicalNotes
      })
    });

    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      setTimeout(() => {
        window.location.href = `/print/${currentRecordId}`;
      }, 800);
    } else {
      showToast(data.message, 'error');
    }
  } catch (err) {
    console.error('Error signing record:', err);
    showToast('Failed to save electronic signature.', 'error');
  }
}
