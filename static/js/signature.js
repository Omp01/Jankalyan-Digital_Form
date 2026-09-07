/**
 * Jankalyan Blood Bank System - E-Signature Canvas Controller
 */

let canvas = null;
let ctx = null;
let isDrawing = false;
let hasSignature = false;

function initSignaturePad() {
  canvas = document.getElementById('signatureCanvas');
  if (!canvas) return;

  ctx = canvas.getContext('2d');
  resizeCanvas();

  canvas.addEventListener('pointerdown', startDrawing);
  canvas.addEventListener('pointermove', draw);
  canvas.addEventListener('pointerup', stopDrawing);
  canvas.addEventListener('pointercancel', stopDrawing);
  canvas.addEventListener('mouseleave', stopDrawing);

  window.addEventListener('resize', resizeCanvas);
}

function resizeCanvas() {
  if (!canvas) return;
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;

  let tempImage = null;
  if (hasSignature) {
    tempImage = canvas.toDataURL();
  }

  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;
  ctx.scale(dpr, dpr);

  ctx.strokeStyle = '#0F172A';
  ctx.lineWidth = 2.5;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';

  if (tempImage) {
    const img = new Image();
    img.src = tempImage;
    img.onload = () => ctx.drawImage(img, 0, 0, rect.width, rect.height);
  } else {
    clearSignature();
  }
}

function getPointerPos(evt) {
  const rect = canvas.getBoundingClientRect();
  return {
    x: evt.clientX - rect.left,
    y: evt.clientY - rect.top
  };
}

function startDrawing(evt) {
  evt.preventDefault();
  isDrawing = true;
  const pos = getPointerPos(evt);
  ctx.beginPath();
  ctx.moveTo(pos.x, pos.y);
}

function draw(evt) {
  if (!isDrawing) return;
  evt.preventDefault();
  const pos = getPointerPos(evt);
  ctx.lineTo(pos.x, pos.y);
  ctx.stroke();
  hasSignature = true;
}

function stopDrawing(evt) {
  if (isDrawing) {
    ctx.closePath();
    isDrawing = false;
  }
}

function clearSignature() {
  if (!canvas || !ctx) return;
  const rect = canvas.getBoundingClientRect();
  ctx.clearRect(0, 0, rect.width, rect.height);
  hasSignature = false;
}

async function confirmAndFinaliseRecord() {
  if (!hasSignature) {
    showToast('Please provide an electronic signature before finalising.', 'error');
    return;
  }

  if (!currentRecordId) {
    const saved = await saveRecord(true);
    if (!saved) return;
  }

  const signatureData = canvas.toDataURL('image/png');
  const medicalNotes = document.getElementById('medical_notes')?.value || '';

  try {
    const res = await fetch(`/api/records/${currentRecordId}/sign`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        signature_data: signatureData,
        medical_notes: medicalNotes
      })
    });

    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      setTimeout(() => {
        window.location.href = `/print/${currentRecordId}`;
      }, 1000);
    } else {
      showToast(data.message, 'error');
    }
  } catch (err) {
    console.error('Error signing record:', err);
    showToast('Failed to save electronic signature.', 'error');
  }
}
