/**
 * Jankalyan Blood Bank System - Bilingual Translation Engine
 * Form reference: QF/JKRP/18 (English & Marathi)
 */

const I18N = {
  en: {
    system_title: "Jankalyan Blood Centre",
    system_subtitle: "Blood Bank Digital Form System (QF/JKRP/18)",
    nav_dashboard: "Dashboard",
    nav_new_form: "New Donor Form",
    nav_records: "Search Records",
    nav_users: "Manage Users",
    nav_audit: "Audit Logs",
    nav_logout: "Logout",
    lang_en: "English",
    lang_mr: "मराठी",
    welcome_user: "Welcome",
    role_admin: "Administrator",
    role_staff: "Blood Bank Staff",
    role_doctor: "Medical Officer",
    footer_powered_by: "Powered by Harbinger Group",

    // Common Buttons
    btn_previous: "Previous",
    btn_next: "Next",
    btn_save_draft: "Save Draft",
    btn_submit_verification: "Submit for Verification",
    btn_sign_finalise: "Confirm & Finalise",
    btn_clear: "Clear",
    btn_cancel: "Cancel",
    btn_search: "Search Records",
    btn_export_excel: "Export to Excel",
    btn_print: "Print A4 Form",
    btn_view: "View Record",
    btn_edit: "Edit Record",
    btn_unlock: "Unlock Record",

    // Step Headers
    step_1: "1. Donor Demographics",
    step_2: "2. Medical Examination",
    step_3: "3. Medication & Disease History",
    step_4: "4. Deferral & Symptoms",
    step_5: "5. Blood Bag",
    step_6: "6. Consent & Verification",

    // Step 1 Labels
    record_number: "Record Number",
    donor_number: "Donor ID",
    donation_date: "Date of Donation",
    full_name: "Full Name (First Name Father/Husband Name Surname)",
    gender: "Gender",
    gender_male: "Male",
    gender_female: "Female",
    gender_others: "Others",
    date_of_birth: "Date of Birth",
    age: "Age (Years)",
    occupation: "Occupation",
    organization_company: "Organization / Camp Name",
    residential_address: "Residential Address",
    city_district: "City / District",
    pincode: "Pincode",
    mobile_number: "Mobile Number",
    email: "Email Address",
    blood_group_known: "Known Blood Group",
    donation_type: "Type of Donation",
    donation_type_voluntary: "Voluntary",
    donation_type_replacement: "Replacement",
    donation_type_autologous: "Autologous",
    last_donation_date: "Date of Last Donation",
    number_of_past_donations: "Total Past Donations",

    // Step 2 Medical Exam
    weight_kg: "Weight (kg)",
    height_cm: "Height (cm)",
    pulse_rate: "Pulse Rate (bpm)",
    bp_systolic: "BP Systolic (mmHg)",
    bp_diastolic: "BP Diastolic (mmHg)",
    hemoglobin_g_dl: "Hemoglobin (g/dL)",
    body_temperature: "Body Temperature (°F)",
    skin_site_inspection: "Venepuncture Site Inspection",
    inspection_satisfactory: "Satisfactory",
    inspection_unsatisfactory: "Unsatisfactory",
    screening_outcome: "Pre-donation Screening Result",
    outcome_eligible: "ELIGIBLE (पात्र)",
    outcome_deferred: "DEFERRED (स्थगिती)",
    outcome_rejected: "REJECTED (अयोग्य)",
    deferral_reason: "Deferral Reason",
    deferral_duration: "Deferral Duration",

    // Step 3 Medication History Table Headers
    med_timeframe: "Timeframe / Duration",
    med_question: "Medication / Condition Question",
    med_answer: "Yes / No",
    yes: "Yes",
    no: "No",

    // Step 4 Deferral Checklist & High Risk
    permanent_deferral_title: "13. Permanent Deferral Conditions Checkbox Grid",
    permanent_deferral_desc: "Check (✓) if the donor has history of any of the following conditions:",
    high_risk_title: "14. Personal High-Risk History",
    symptoms_title: "15. Recent Symptoms History",
    female_title: "16. For Female Donors",
    next24h_title: "17. Next 24 Hours High-Risk Occupation / Duty",

    // Step 5 Blood Bag
    blood_bag_number: "Blood Bag Barcode / Number",
    bag_type: "Type of Bag",
    bag_single: "Single Bag (350ml/450ml)",
    bag_double: "Double Bag",
    bag_triple: "Triple Bag",
    bag_quadruple: "Quadruple Bag",
    anticoagulant: "Anticoagulant Solution",
    volume_ml: "Volume Collected (mL)",
    segment_number: "Segment Number",
    phlebotomy_site: "Phlebotomy Site",
    site_right: "Right Arm",
    site_left: "Left Arm",
    phlebotomist_staff_id: "Phlebotomist Staff Name",
    adverse_reaction: "Adverse Donor Reaction",
    reaction_none: "None",
    reaction_dizziness: "Dizziness / Giddiness",
    reaction_fainting: "Fainting / Syncope",
    reaction_hematoma: "Hematoma at Injection Site",
    reaction_other: "Other (Specify below)",

    // Step 6 Consent & Signature
    consent_title: "Donor Consent Form (मान्यतापत्र)",
    consent_item1: "1) I understand that blood donation is a totally voluntary act and no inducement or remuneration has been offered.",
    consent_item2: "2) I hereby give consent to utilize my plasma / blood components for patients or other blood storage centres.",
    consent_item3: "3) I have read and understood all information presented and answered all questions truthfully.",
    consent_item4: "4) I consent to testing of my blood for HIV, Hepatitis B/C, Syphilis, and Malaria.",
    consent_item5: "5) Would you like to be informed about any abnormal test result?",
    mo_verification_title: "Medical Officer Verification & Electronic Signature",
    medical_notes: "Clinical Notes / Remarks by Medical Officer",
    mo_signature_label: "Medical Officer Electronic Signature Pad",
    record_status_locked: "Record Finalised & Locked",

    // Messages
    msg_saved_draft: "Draft saved successfully.",
    msg_submitted: "Form submitted for Medical Verification.",
    msg_signed: "Record verified and signed successfully.",
    msg_fill_required: "Please fill in all required fields marked with *"
  },

  mr: {
    system_title: "जनकल्याण रक्तकेंद्र",
    system_subtitle: "रक्तपेढी संगणकीय फॉर्म प्रणाली (QF/JKRP/18)",
    nav_dashboard: "डॅशबोर्ड",
    nav_new_form: "नवीन फॉर्म",
    nav_records: "रक्तदाता नोंदी",
    nav_users: "वापरकर्ते व्यवस्थापन",
    nav_audit: "ऑडिट लॉग्स",
    nav_logout: "लॉगआउट",
    lang_en: "English",
    lang_mr: "मराठी",
    welcome_user: "स्वागत आहे",
    role_admin: "प्रशासक (Admin)",
    role_staff: "रक्तपेढी कर्मचारी",
    role_doctor: "वैद्यकीय अधिकारी (Medical Officer)",
    footer_powered_by: "Powered by Harbinger Group",

    // Common Buttons
    btn_previous: "मागे",
    btn_next: "पुढे",
    btn_save_draft: "मसुदा जतन करा (Save Draft)",
    btn_submit_verification: "पडताळणीसाठी सादर करा",
    btn_sign_finalise: "स्वीकृत करा व अंतिम करा",
    btn_clear: "पुसा (Clear)",
    btn_cancel: "रद्द करा",
    btn_search: "शोध घ्या",
    btn_export_excel: "Excel मध्ये पाठवा (Export)",
    btn_print: "A4 फॉर्म मुद्रित करा (Print)",
    btn_view: "पहा (View)",
    btn_edit: "संपादित करा",
    btn_unlock: "अनलॉक करा",

    // Step Headers
    step_1: "१. रक्तदाता प्राथमिक माहिती",
    step_2: "२. वैद्यकीय तपासणी",
    step_3: "३. औषध व आजार इतिहास (प्रश्नावली)",
    step_4: "४. कायमस्वरूपी स्थगिती व लक्षणे",
    step_5: "५. रक्त संकलन व बॅग तपशील",
    step_6: "६. मान्यतापत्र व वैद्यकीय स्वाक्षरी",

    // Step 1 Labels
    record_number: "नोंदणी क्रमांक",
    donor_number: "रक्तदाता क्रमांक",
    donation_date: "दानाची तारीख",
    full_name: "संपूर्ण नाव (नाव वडिलांचे/पतीचे नाव आडनाव)",
    gender: "लिंग",
    gender_male: "पुरुष",
    gender_female: "स्त्री",
    gender_others: "इतर (Others)",
    date_of_birth: "जन्म तारीख",
    age: "वय (वर्षे)",
    occupation: "व्यवसाय",
    organization_company: "संस्था / कंपनी / शिबीर नाव",
    residential_address: "निवासी पत्ता",
    city_district: "शहर / जिल्हा",
    pincode: "पिन कोड",
    mobile_number: "मोबाईल क्रमांक",
    email: "ईमेल आयडी",
    blood_group_known: "माहित असलेला रक्तगट",
    donation_type: "दानाचा प्रकार",
    donation_type_voluntary: "ऐच्छिक (Voluntary)",
    donation_type_replacement: "बदली (Replacement)",
    donation_type_autologous: "स्वयं-दान (Autologous)",
    last_donation_date: "शेवटच्या दानाची तारीख",
    number_of_past_donations: "एकूण मागील रक्तदान",

    // Step 2 Medical Exam
    weight_kg: "वजन (कि.ग्रॅ.)",
    height_cm: "उंची (से.मी.)",
    pulse_rate: "नाडीचे ठोके (प्रति मि.)",
    bp_systolic: "रक्तदाब सिस्टोलिक (mmHg)",
    bp_diastolic: "रक्तदाब डायस्टोलिक (mmHg)",
    hemoglobin_g_dl: "हिमोग्लोबिन (ग्रॅम/डेसी.लि.)",
    body_temperature: "शारीरिक तापमान (°फॅ)",
    skin_site_inspection: "शिरा / त्वचा तपासणी",
    inspection_satisfactory: "समाधानकारक",
    inspection_unsatisfactory: "असमाधानकारक",
    screening_outcome: "पूर्व-तपासणी निकाल",
    outcome_eligible: "पात्र (ELIGIBLE)",
    outcome_deferred: "स्थगिती (DEFERRED)",
    outcome_rejected: "अयोग्य (REJECTED)",
    deferral_reason: "स्थगितीचे कारण",
    deferral_duration: "स्थगितीचा कालावधी",

    // Step 3 Medication History Table Headers
    med_timeframe: "कालावधी / वेळ",
    med_question: "औषध / आजार माहिती",
    med_answer: "होय / नाही",
    yes: "होय",
    no: "नाही",

    // Step 4 Deferral Checklist & High Risk
    permanent_deferral_title: "१३. रक्तदानास कायमस्वरूपी स्थगिती (कृपया टिक करा ✓)",
    permanent_deferral_desc: "भूतकाळात खालीलपैकी कोणत्याही आजारातून गेला असाल तर टिक करा:",
    high_risk_title: "१४. वैयक्तिक माहिती / धोकादायक पार्श्वभूमी",
    symptoms_title: "१५. अलीकडची लक्षणे",
    female_title: "१६. महिलांसाठी विशेष प्रश्न",
    next24h_title: "१७. पुढील २४ तासांत अतिश्रमाचे / आपत्कालीन काम",

    // Step 5 Blood Bag
    blood_bag_number: "रक्त पिशवी क्रमांक (Barcode)",
    bag_type: "बॅगचा प्रकार",
    bag_single: "सिंगल बॅग (Single 350/450 ml)",
    bag_double: "डबल बॅग (Double Bag)",
    bag_triple: "ट्रिपल बॅग (Triple Bag)",
    bag_quadruple: "क्वाडड्रपल बॅग (Quadruple Bag)",
    anticoagulant: "अँटीकोआगुलंट द्रावण",
    volume_ml: "संकलित रक्ताचे प्रमाण (मि.ली.)",
    segment_number: "सेगमेंट क्रमांक",
    phlebotomy_site: "रक्तदान शिरा (हात)",
    site_right: "उजवा हात (Right Arm)",
    site_left: "डावा हात (Left Arm)",
    phlebotomist_staff_id: "रक्तदान घेणारे कर्मचारी",
    adverse_reaction: "रक्तदात्याला झालेला त्रास",
    reaction_none: "काही नाही",
    reaction_dizziness: "चक्कर येणे",
    reaction_fainting: "मूर्च्छा येणे",
    reaction_hematoma: "सुई टोचलेल्या जागी सूज",
    reaction_other: "इतर (खाली नमूद करा)",

    // Step 6 Consent & Signature
    consent_title: "मान्यतापत्र (Donor Consent)",
    consent_item1: "१) मला हे पूर्णपणे समजले आहे की रक्तदान हे पूर्णतः स्वच्छेने करायचे आहे व त्यासाठी कोणताही मोबदला दिलेला नाही.",
    consent_item2: "२) प्लाझ्मा फ्रॅक्शनेशन व इतर रुग्णांसाठी किंवा इतर रक्तपेढ्यांना वापरण्यास मी अनुमती देत आहे.",
    consent_item3: "३) मी सर्व प्रश्नांची उत्तरे विचारपूर्वक व बरोबर दिली आहेत. चुकीची माहिती लपवल्यास होणाऱ्या परिणामांची मला जाणीव आहे.",
    consent_item4: "४) माझ्या रक्तावर एच.आय.व्ही/एड्स, हिपॅटायटीस बी/सी, सिफिलीस व मलेरिया या चाचण्या केल्या जातील याची मला जाणीव आहे.",
    consent_item5: "५) या तपासण्यांमधील काही तपासण्या दोषपूर्ण आढळल्यास आपणास कळवावे का?",
    mo_verification_title: "वैद्यकीय अधिकारी पडताळणी व ई-स्वाक्षरी",
    medical_notes: "वैद्यकीय अधिकाऱ्याची टीप / अभिप्राय",
    mo_signature_label: "वैद्यकीय अधिकारी इलेक्ट्रॉनिक स्वाक्षरी पॅड",
    record_status_locked: "नोंदणी अंतिम व लॉक झाली आहे",

    // Messages
    msg_saved_draft: "मसुदा यशस्वीरित्या जतन केला.",
    msg_submitted: "फॉर्म वैद्यकीय पडताळणीसाठी सादर केला.",
    msg_signed: "नोंदणी स्वीकृत व स्वाक्षरी झाली.",
    msg_fill_required: "कृपया सर्व आवश्यक (*) रकाने भरा."
  }
};

let currentLang = localStorage.getItem('app_lang') || 'en';

function getTranslation(key) {
  if (I18N[currentLang] && I18N[currentLang][key]) {
    return I18N[currentLang][key];
  }
  if (I18N['en'][key]) {
    return I18N['en'][key];
  }
  return key;
}

function setLanguage(lang) {
  if (lang !== 'en' && lang !== 'mr') return;
  currentLang = lang;
  localStorage.setItem('app_lang', lang);
  applyTranslations();
  window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang } }));
}

function applyTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const translation = getTranslation(key);
    if (el.tagName === 'INPUT' && el.getAttribute('placeholder')) {
      el.setAttribute('placeholder', translation);
    } else {
      el.innerHTML = translation;
    }
  });

  const btnEn = document.getElementById('btnLangEn');
  const btnMr = document.getElementById('btnLangMr');
  if (btnEn && btnMr) {
    if (currentLang === 'en') {
      btnEn.classList.add('active');
      btnMr.classList.remove('active');
    } else {
      btnMr.classList.add('active');
      btnEn.classList.remove('active');
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  applyTranslations();
});
