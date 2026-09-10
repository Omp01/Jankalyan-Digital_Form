/**
 * Jankalyan Blood Bank System - Form Stepper & Controller (QF/JKRP/18)
 */

let currentStep = 1;
let currentRecordId = null;
let isRecordLocked = false;

document.addEventListener('DOMContentLoaded', () => {
  initFormEvents();
  checkEditRecordMode();
});

function checkEditRecordMode() {
  const urlParams = new URLSearchParams(window.location.search);
  const id = urlParams.get('id');
  if (id) {
    currentRecordId = parseInt(id);
    loadRecordData(currentRecordId);
  } else {
    const today = new Date().toISOString().split('T')[0];
    const dateElem = document.getElementById('donation_date');
    if (dateElem) dateElem.value = today;
  }
}

function initFormEvents() {
  const dobElem = document.getElementById('date_of_birth');
  if (dobElem) {
    dobElem.addEventListener('change', (e) => {
      if (e.target.value) {
        const birthDate = new Date(e.target.value);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const m = today.getMonth() - birthDate.getMonth();
        if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
          age--;
        }
        document.getElementById('age').value = age > 0 ? age : 18;
      }
    });
  }

  ['weight_kg', 'hemoglobin_g_dl', 'bp_systolic', 'bp_diastolic'].forEach(id => {
    const elem = document.getElementById(id);
    if (elem) {
      elem.addEventListener('input', validateMedicalEligibility);
    }
  });

  document.querySelectorAll('.btn-group-toggle label').forEach(label => {
    label.addEventListener('click', function() {
      const parent = this.closest('.btn-group-toggle');
      parent.querySelectorAll('label').forEach(l => l.classList.remove('active'));
      this.classList.add('active');
    });
  });
}

function validateMedicalEligibility() {
  const weight = parseFloat(document.getElementById('weight_kg')?.value || 0);
  const hb = parseFloat(document.getElementById('hemoglobin_g_dl')?.value || 0);
  const sBP = parseInt(document.getElementById('bp_systolic')?.value || 0);
  const dBP = parseInt(document.getElementById('bp_diastolic')?.value || 0);

  const alertBox = document.getElementById('eligibilityAlert');
  if (!alertBox) return;

  let warnings = [];
  if (weight > 0 && weight < 45) {
    warnings.push("Weight is below minimum 45 kg requirement (वजन ४५ कि.ग्रॅ. पेक्षा कमी आहे).");
  }
  if (hb > 0 && hb < 12.5) {
    warnings.push("Hemoglobin is below minimum 12.5 g/dL requirement (हिमोग्लोबिन १२.५ पेक्षा कमी आहे).");
  }
  if (sBP > 0 && (sBP < 100 || sBP > 140)) {
    warnings.push("Systolic BP is out of normal range 100-140 mmHg (सिस्टोलिक रक्तदाब सामान्य मर्यादेबाहेर आहे).");
  }
  if (dBP > 0 && (dBP < 60 || dBP > 90)) {
    warnings.push("Diastolic BP is out of normal range 60-90 mmHg (डायस्टोलिक रक्तदाब सामान्य मर्यादेबाहेर आहे).");
  }

  if (warnings.length > 0) {
    alertBox.style.display = 'block';
    alertBox.innerHTML = `⚠️ <strong>Medical Eligibility Notice:</strong><br>${warnings.join('<br>')}`;
  } else {
    alertBox.style.display = 'none';
  }
}

function goToStep(step) {
  if (step < 1 || step > 6) return;

  if (step > currentStep && currentStep === 1) {
    const fullName = document.getElementById('full_name')?.value?.trim();
    const mobile = document.getElementById('mobile_number')?.value?.trim();
    if (!fullName || !mobile) {
      showToast(getTranslation('msg_fill_required'), 'error');
      return;
    }
  }

  document.querySelectorAll('.form-step').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.stepper-item').forEach(st => st.classList.remove('active', 'completed'));

  const nextStepElem = document.getElementById(`step-${step}`);
  if (nextStepElem) nextStepElem.classList.add('active');

  for (let i = 1; i <= 6; i++) {
    const item = document.getElementById(`step-indicator-${i}`);
    if (!item) continue;
    if (i < step) item.classList.add('completed');
    if (i === step) item.classList.add('active');
  }

  currentStep = step;
  window.scrollTo({ top: 0, behavior: 'smooth' });

  if (step === 6) {
    renderReviewSummary();
    if (typeof initSignaturePad === 'function') {
      initSignaturePad();
    }
  }
}

function getFormData() {
  const getSelectVal = (name) => {
    const elem = document.querySelector(`select[name="${name}"]`);
    return elem ? elem.value : 'No';
  };

  const permDef = [];
  document.querySelectorAll('input[name="perm_deferral"]:checked').forEach(cb => {
    permDef.push(cb.value);
  });

  const quest = {
    // Page 1 Questions 1 to 10
    q1_age_18_65: getSelectVal('q1_age_18_65'),
    q2_meals_4h: getSelectVal('q2_meals_4h'),
    q3a_slept_well: getSelectVal('q3a_slept_well'),
    q3b_night_shift_sleep: getSelectVal('q3b_night_shift_sleep'),
    q4_heavy_work_12h: getSelectVal('q4_heavy_work_12h'),
    q5_malaise_weakness: getSelectVal('q5_malaise_weakness'),
    q6_cough_cold_mood: getSelectVal('q6_cough_cold_mood'),
    q7_alcohol_24h: getSelectVal('q7_alcohol_24h'),
    q8_loose_motions_15d: getSelectVal('q8_loose_motions_15d'),
    q9_migraine_weekly: getSelectVal('q9_migraine_weekly'),
    q10_daily_meds: getSelectVal('q10_daily_meds'),

    // Page 2 & 3 Questions (11 to 17)
    q11a_endoscopy_sampling: getSelectVal('q11a_endoscopy_sampling'),
    q11b_endoscopy_malignant: getSelectVal('q11b_endoscopy_malignant'),
    q11b_endoscopy_benign: getSelectVal('q11b_endoscopy_benign'),
    q11c_endoscopy_other: getSelectVal('q11c_endoscopy_other'),

    q12a_male_3months: getSelectVal('q12a_male_3months'),
    q12b_female_4months: getSelectVal('q12b_female_4months'),
    q12c_donation_trouble: getSelectVal('q12c_donation_trouble'),
    q12d_platelets_28days: getSelectVal('q12d_platelets_28days'),

    q14a_hiv_diagnosis: getSelectVal('q14a_hiv_diagnosis'),
    q14b_unsafe_sex: getSelectVal('q14b_unsafe_sex'),
    q14c_injected_narcotics: getSelectVal('q14c_injected_narcotics'),
    q14d_partner_risk: getSelectVal('q14d_partner_risk'),

    q15a_night_sweats: getSelectVal('q15a_night_sweats'),
    q15b_persistent_fever: getSelectVal('q15b_persistent_fever'),
    q15c_swollen_glands: getSelectVal('q15c_swollen_glands'),
    q15d_persistent_diarrhea: getSelectVal('q15d_persistent_diarrhea'),
    q15e_weight_loss: getSelectVal('q15e_weight_loss'),

    q16a_female_abortion: getSelectVal('q16a_female_abortion'),
    q16b_female_pregnant: getSelectVal('q16b_female_pregnant'),
    q16c_female_delivery: getSelectVal('q16c_female_delivery'),
    q16d_female_breastfeeding: getSelectVal('q16d_female_breastfeeding'),
    q16e_female_periods: getSelectVal('q16e_female_periods'),
    q16f_female_pcod: getSelectVal('q16f_female_pcod'),

    q17a_air_crew: getSelectVal('q17a_air_crew'),
    q17b_long_driver: getSelectVal('q17b_long_driver'),
    q17c_strenuous_work: getSelectVal('q17c_strenuous_work'),
    q17d_emergency_service: getSelectVal('q17d_emergency_service'),
    q17e_altitude_diving: getSelectVal('q17e_altitude_diving'),
    q17f_past_12h_duties: getSelectVal('q17f_past_12h_duties'),

    // Medication history
    med_daily_thyroid: getSelectVal('med_daily_thyroid'),
    med_3days_aspirin: getSelectVal('med_3days_aspirin'),
    med_7days_antifungals: getSelectVal('med_7days_antifungals'),
    med_2weeks_antibiotics: getSelectVal('med_2weeks_antibiotics'),
    med_28days_vaccines: getSelectVal('med_28days_vaccines'),
    med_1month_acne_prostate: getSelectVal('med_1month_acne_prostate'),
    med_3months_malaria: getSelectVal('med_3months_malaria'),
    med_6months_radioactive: getSelectVal('med_6months_radioactive'),
    med_1year_rabies_tattoo: getSelectVal('med_1year_rabies_tattoo'),
    med_2years_tb: getSelectVal('med_2years_tb')
  };

  return {
    record_id: currentRecordId,
    donor: {
      donor_number: document.getElementById('donor_number')?.value || '',
      donation_date: document.getElementById('donation_date')?.value || '',
      full_name: document.getElementById('full_name')?.value || '',
      gender: document.querySelector('input[name="gender"]:checked')?.value || 'Male',
      date_of_birth: document.getElementById('date_of_birth')?.value || '',
      age: parseInt(document.getElementById('age')?.value || 18),
      occupation: document.getElementById('occupation')?.value || '',
      organization_company: document.getElementById('organization_company')?.value || '',
      residential_address: document.getElementById('residential_address')?.value || '',
      city_district: document.getElementById('city_district')?.value || '',
      pincode: document.getElementById('pincode')?.value || '',
      mobile_number: document.getElementById('mobile_number')?.value || '',
      email: document.getElementById('email')?.value || '',
      blood_group_known: document.getElementById('blood_group_known')?.value || 'Unknown',
      donation_type: document.getElementById('donation_type')?.value || 'Voluntary',
      last_donation_date: document.getElementById('last_donation_date')?.value || '',
      number_of_past_donations: parseInt(document.getElementById('number_of_past_donations')?.value || 0)
    },
    medical_exam: {
      weight_kg: parseFloat(document.getElementById('weight_kg')?.value || 50),
      height_cm: parseFloat(document.getElementById('height_cm')?.value || 165),
      pulse_rate: parseInt(document.getElementById('pulse_rate')?.value || 72),
      bp_systolic: parseInt(document.getElementById('bp_systolic')?.value || 120),
      bp_diastolic: parseInt(document.getElementById('bp_diastolic')?.value || 80),
      hemoglobin_g_dl: parseFloat(document.getElementById('hemoglobin_g_dl')?.value || 13.5),
      body_temperature: parseFloat(document.getElementById('body_temperature')?.value || 98.6),
      skin_site_inspection: document.querySelector('input[name="skin_site_inspection"]:checked')?.value || 'Satisfactory',
      screening_outcome: document.querySelector('input[name="screening_outcome"]:checked')?.value || 'ELIGIBLE',
      deferral_reason: document.getElementById('deferral_reason')?.value || '',
      deferral_duration: document.getElementById('deferral_duration')?.value || ''
    },
    medication_history: quest,
    permanent_deferrals: permDef,
    questionnaire_answers: quest,
    consent: {
      consent_given: document.getElementById('consent_given')?.checked ?? true,
      abnormal_results_notify: document.getElementById('abnormal_results_notify')?.checked ?? true,
      donor_signature_data: (() => {
        const dCanvas = document.getElementById('donorSignatureCanvas');
        if (window.hasDonorSignature && dCanvas) {
          return dCanvas.toDataURL('image/png');
        }
        if (window.loadedDonorSignature) {
          return window.loadedDonorSignature;
        }
        if (dCanvas) {
          const dataUrl = dCanvas.toDataURL('image/png');
          if (dataUrl && dataUrl.length > 1000) return dataUrl;
        }
        return '';
      })()
    },
    donation_details: {
      blood_bag_number: document.getElementById('blood_bag_number')?.value || '',
      bag_type: document.getElementById('bag_type')?.value || 'Single',
      anticoagulant: document.getElementById('anticoagulant')?.value || 'CPDA-1',
      volume_ml: parseInt(document.getElementById('volume_ml')?.value || 350),
      bag_manufacturer: document.getElementById('bag_manufacturer')?.value || 'FK',
      batch_number: document.getElementById('batch_number')?.value || '',
      segment_number: document.getElementById('segment_number')?.value || '',
      counselor_name: document.getElementById('counselor_name')?.value || '',
      collection_duration: document.getElementById('collection_duration')?.value || '10',
      phlebotomy_site: document.getElementById('phlebotomy_site')?.value || 'Right Arm',
      phlebotomist_staff_id: document.getElementById('phlebotomist_staff_id')?.value || '',
      donation_status: document.getElementById('donation_status')?.value || 'SUCCESSFUL',
      adverse_reaction: document.getElementById('adverse_reaction')?.value || 'NONE',
      reaction_details: document.getElementById('reaction_details')?.value || ''
    }
  };
}

async function saveRecord(asDraft = true) {
  const payload = getFormData();
  payload.save_as_draft = asDraft;

  try {
    const res = await fetch('/api/records', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    if (result.success) {
      currentRecordId = result.record_id;
      showToast(result.message, 'success');
      if (asDraft) {
        document.getElementById('recNumDisplay').innerText = result.record_number;
      }
      return result;
    } else {
      showToast(result.message, 'error');
      return null;
    }
  } catch (err) {
    console.error('Error saving record:', err);
    showToast('Failed to save record. Server error.', 'error');
    return null;
  }
}

async function submitForVerification() {
  const saved = await saveRecord(false);
  if (saved) {
    try {
      const res = await fetch(`/api/records/${currentRecordId}/submit`, { method: 'POST' });
      const data = await res.json();
      if (data.success) {
        showToast(data.message, 'success');
        setTimeout(() => {
          window.location.href = '/records.html';
        }, 1200);
      } else {
        showToast(data.message, 'error');
      }
    } catch (err) {
      console.error(err);
    }
  }
}

async function loadRecordData(recordId) {
  try {
    const res = await fetch(`/api/records/${recordId}`);
    const data = await res.json();
    if (!data.success) {
      showToast('Failed to load record', 'error');
      return;
    }

    const { record, donor, medical_exam, medication_history, permanent_deferrals, questionnaire_answers, consent, donation_details, signature } = data;

    if (record.status === 'SIGNED' || record.status === 'COMPLETED') {
      isRecordLocked = true;
      document.getElementById('lockedNotice')?.classList.remove('hidden');
    }

    if (donor) {
      document.getElementById('recNumDisplay').innerText = record.record_number;
      if (document.getElementById('donor_number')) document.getElementById('donor_number').value = donor.donor_number || '';
      if (document.getElementById('donation_date')) document.getElementById('donation_date').value = formatDateForInput(record.donation_date) || '';
      if (document.getElementById('full_name')) document.getElementById('full_name').value = donor.full_name || '';
      if (document.getElementById('date_of_birth')) document.getElementById('date_of_birth').value = formatDateForInput(donor.date_of_birth) || '';
      if (document.getElementById('age')) document.getElementById('age').value = donor.age || 18;
      if (document.getElementById('occupation')) document.getElementById('occupation').value = donor.occupation || '';
      if (document.getElementById('organization_company')) document.getElementById('organization_company').value = donor.organization_company || '';
      if (document.getElementById('residential_address')) document.getElementById('residential_address').value = donor.residential_address || '';
      if (document.getElementById('city_district')) document.getElementById('city_district').value = donor.city_district || '';
      if (document.getElementById('pincode')) document.getElementById('pincode').value = donor.pincode || '';
      if (document.getElementById('mobile_number')) document.getElementById('mobile_number').value = donor.mobile_number || '';
      if (document.getElementById('email')) document.getElementById('email').value = donor.email || '';
      if (document.getElementById('blood_group_known')) document.getElementById('blood_group_known').value = donor.blood_group_known || 'Unknown';
      if (document.getElementById('donation_type')) document.getElementById('donation_type').value = donor.donation_type || 'Voluntary';

      const genderRadio = document.querySelector(`input[name="gender"][value="${donor.gender}"]`);
      if (genderRadio) genderRadio.checked = true;
    }

    if (medical_exam) {
      if (document.getElementById('weight_kg')) document.getElementById('weight_kg').value = medical_exam.weight_kg || '';
      if (document.getElementById('height_cm')) document.getElementById('height_cm').value = medical_exam.height_cm || '';
      if (document.getElementById('pulse_rate')) document.getElementById('pulse_rate').value = medical_exam.pulse_rate || '';
      if (document.getElementById('bp_systolic')) document.getElementById('bp_systolic').value = medical_exam.bp_systolic || '';
      if (document.getElementById('bp_diastolic')) document.getElementById('bp_diastolic').value = medical_exam.bp_diastolic || '';
      if (document.getElementById('hemoglobin_g_dl')) document.getElementById('hemoglobin_g_dl').value = medical_exam.hemoglobin_g_dl || '';
      if (document.getElementById('body_temperature')) document.getElementById('body_temperature').value = medical_exam.body_temperature || '';

      const outcomeRadio = document.querySelector(`input[name="screening_outcome"][value="${medical_exam.screening_outcome}"]`);
      if (outcomeRadio) outcomeRadio.checked = true;
    }

    if (donation_details) {
      if (document.getElementById('blood_bag_number')) document.getElementById('blood_bag_number').value = donation_details.blood_bag_number || '';
      if (document.getElementById('bag_type')) document.getElementById('bag_type').value = donation_details.bag_type || 'Single';
      if (document.getElementById('anticoagulant')) document.getElementById('anticoagulant').value = donation_details.anticoagulant || 'CPDA-1';
      if (document.getElementById('volume_ml')) document.getElementById('volume_ml').value = donation_details.volume_ml || 350;
      if (document.getElementById('phlebotomist_staff_id')) document.getElementById('phlebotomist_staff_id').value = donation_details.phlebotomist_staff_id || '';
    }

    if (permanent_deferrals && Array.isArray(permanent_deferrals)) {
      permanent_deferrals.forEach(val => {
        const cb = document.querySelector(`input[name="perm_deferral"][value="${val}"]`);
        if (cb) cb.checked = true;
      });
    }

    if (consent) {
      if (document.getElementById('consent_given')) document.getElementById('consent_given').checked = consent.consent_given !== false;
      if (document.getElementById('abnormal_results_notify')) document.getElementById('abnormal_results_notify').checked = consent.abnormal_results_notify !== false;

      if (consent.donor_signature_data) {
        window.loadedDonorSignature = consent.donor_signature_data;
        const dCanvas = document.getElementById('donorSignatureCanvas');
        if (dCanvas) {
          const dCtx = dCanvas.getContext('2d');
          const img = new Image();
          img.onload = () => {
            dCtx.clearRect(0, 0, dCanvas.width, dCanvas.height);
            dCtx.drawImage(img, 0, 0, dCanvas.width, dCanvas.height);
          };
          img.src = consent.donor_signature_data;
        }
      }
    }

    validateMedicalEligibility();
  } catch (err) {
    console.error('Error loading record:', err);
  }
}

function renderReviewSummary() {
  const container = document.getElementById('reviewSummaryContent');
  if (!container) return;

  const data = getFormData();
  container.innerHTML = `
    <div class="review-box">
      <h3>📋 ${data.donor.full_name} (${data.donor.gender}, ${data.donor.age} yrs)</h3>
      <p><strong>Donation Date:</strong> ${formatDate(data.donor.donation_date)} | <strong>DOB:</strong> ${formatDate(data.donor.date_of_birth) || 'N/A'}</p>
      <p><strong>Mobile:</strong> ${data.donor.mobile_number} | <strong>City:</strong> ${data.donor.city_district}</p>
      <p><strong>Blood Group:</strong> ${data.donor.blood_group_known} | <strong>Donation Type:</strong> ${data.donor.donation_type}</p>
      <hr>
      <h4>🩺 Medical Exam:</h4>
      <p><strong>Weight:</strong> ${data.medical_exam.weight_kg} kg | <strong>Hb:</strong> ${data.medical_exam.hemoglobin_g_dl} g/dL | <strong>BP:</strong> ${data.medical_exam.bp_systolic}/${data.medical_exam.bp_diastolic} mmHg</p>
      <p><strong>Outcome:</strong> <span class="badge badge-${data.medical_exam.screening_outcome.toLowerCase()}">${data.medical_exam.screening_outcome}</span></p>
      <hr>
      <h4>🩸 Blood Bag Details:</h4>
      <p><strong>Bag No:</strong> ${data.donation_details.blood_bag_number || 'N/A'} | <strong>Type:</strong> ${data.donation_details.bag_type} | <strong>Volume:</strong> ${data.donation_details.volume_ml} mL</p>
      ${data.consent && data.consent.donor_signature_data ? `
        <hr>
        <h4>✍️ Donor Signature:</h4>
        <img src="${data.consent.donor_signature_data}" style="max-height:80px; border:1px solid #CBD5E1; padding:4px; background:#fff; border-radius:4px;" alt="Donor Signature">
      ` : ''}
    </div>
  `;
}
