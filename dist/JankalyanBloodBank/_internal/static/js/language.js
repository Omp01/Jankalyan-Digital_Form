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
    btn_modify: "Modify Record",
    btn_edit_user: "Edit User",
    btn_change_password: "Change Password",
    btn_delete_user: "Delete User",
    badge_protected_admin: "Protected Admin",
    title_edit_user: "Edit System User Credentials",
    title_change_password: "Change User Password",

    // Step Headers
    step_1: "1. Donor Demographics",
    step_2: "2. Health Questionnaire",
    step_3: "3. Deferrals & Personal History",
    step_4: "4. Medical Examination",
    step_5: "5. Blood Bag Collection",
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

    // Page 1 Questions (1 to 10) & Staff Details
    q1_age_18_65: "1. Are you within 18-65 years of age?",
    q2_meals_4h: "2. Have you taken breakfast/meals within the last 4 hours?",
    q3a_slept_well: "3A. Have you slept well last night ?",
    q3b_night_shift_sleep: "3B. If you are a night shift worker, have you got undisturbed sleep adequately?",
    q4_heavy_work_12h: "4. Have you been involved in heavy/strenuous work in the last 12 hours?",
    q5_malaise_weakness: "5. Are you having general malaise /pain/weakness today?",
    q6_cough_cold_mood: "6. Are you suffering from cough/cold/sinusitis/conjunctivitis/Anxiety/mood disorders?",
    q7_alcohol_24h: "7. Have you consumed alcohol in the last 24 hours?",
    q8_loose_motions_15d: "8. Have you had loose motions/urinary infection/mumps/measles/chickenpox in the last 15 days ?",
    q9_migraine_weekly: "9. Do you have migraine headache at a frequency of more than once a week?",
    q10_daily_meds: "10. Are you on daily medications for blood pressure, diabetes, or blood thinners (not altered doses in 1 month)?",
    counselor_name: "Pre donation counseling done by",
    bag_manufacturer: "Bag Manufacturer (FK/DT/HLL/Maco/TP/JM)",
    collection_duration: "Duration of blood collection (mins)",
    reaction_management: "Adverse Reaction Management",

    // Table Headers & Controls
    th_no: "No.",
    th_question: "Question Statement (English & Marathi)",
    th_response: "Response",
    opt_yes: "Yes / होय",
    opt_no: "No / नाही",
    med_history_title: "Medication & Disease History (Timeframe Deferral Checklist)",

    // Timeframes
    tf_daily_2m: "Daily Basis (2 months)",
    tf_3days: "In last 3 days",
    tf_7days: "In last 7 days",
    tf_2weeks: "In last 2 Weeks",
    tf_28days: "In last 28 days",
    tf_1month: "In last 1 month",
    tf_3months: "In last 3 months",
    tf_6months: "In last 6 months",
    tf_1year: "In last 1 Year",
    tf_2years: "In last 2 years",

    // Medication Descriptions
    med_daily_thyroid_desc: "Medicines for thyroid disorders (थायरॉईडच्या कमतरतेसाठी औषधे)",
    med_3days_aspirin_desc: "Aspirin or Salicylates (ॲस्पिरिन किंवा सॅलिसिलेट्स)",
    med_7days_antifungals_desc: "Antifungals (Ketoconazole) or Anthelmintics (Mebendazole)",
    med_2weeks_antibiotics_desc: "Antibiotics, steroids, measles/mumps/chickenpox, vaccines (Pertussis, Hep B, Covid Non-live)",
    med_28days_vaccines_desc: "Vaccines (Hep A, Typhoid, Swine flu, Polio, COVID-19 live), Anti-tetanus/venom serum",
    med_1month_acne_prostate_desc: "Acne treatment (Isotretinoin) or Prostate complaint treatment (Finasteride)",
    med_3months_malaria_desc: "Treatment for malaria or Minor Surgery (मलेरिया उपचार / किरकोळ शस्त्रक्रिया)",
    med_6months_radioactive_desc: "Radioactive injection, Dutasteride, Hair transplant / PRP therapy, Dengue/Chikungunya",
    med_1year_rabies_tattoo_desc: "Anti-rabies, Jaundice / Hep A/E, Tattoo / piercing, Blood transfusion / major surgery, Typhoid",
    med_2years_tb_desc: "Tuberculosis (क्षयरोग) or Osteomyelitis (हाडांचा संसर्ग)",

    // Permanent Deferral Checkboxes (15)
    perm_chest_pain: "Chest Pain / Shortness of Breath / Swollen Feet (छातीत दुखणे/पायांना सूज)",
    perm_etretinate: "Treatment with Etretinate (ॲट्रीटिनेट औषध उपचार)",
    perm_ankylosing_spondylosis: "Ankylosing Spondylosis (अँकायलोझिंग स्पॉन्डिलायसिस)",
    perm_asthma_lung: "Asthma & Chronic Obstructive/Restrictive Lung Disease (दमा व फुफ्फुसाचा आजार)",
    perm_kidney_disease: "Chronic Kidney Infection / Failure (मूत्रपिंडाचा आजार)",
    perm_insulin_diabetes: "Insulin Dependent Diabetes / Multi-organ Complications (मधुमेह इन्सुलिन)",
    perm_delayed_faints: "Unexplained Delayed Faints / Faint with Injury / Two Consecutive Faints",
    perm_epilepsy_fits: "Epilepsy / Fits / Seizures / Convulsions (झटके / अपस्मार)",
    perm_heart_disease: "Heart Disease / Surgery / Bypass / Angioplasty / Angina / Rheumatic Heart (हृदयरोग)",
    perm_cancer_cytotoxic: "Cancer / Cytotoxic Drugs / Stem Cells / Organ Transplant (कर्करोग)",
    perm_liver_failure: "Chronic Liver Infection / Failure / Leprosy / Leishmaniasis / Polycythemia Vera",
    perm_hiv_high_risk: "HIV Risk / Transgender / MSM / Sex Workers / Syphilis / Gonorrhea (एच.आय.व्ही धोका)",
    perm_severe_allergy: "Severe Allergy to Betadine/Spirit/Adhesive Bandage (तीव्र ॲलर्जी)",
    perm_thyroid_malignant: "Thyroid Disorders - Thyrotoxicosis / Malignant Tumor / Anti-thyroid drugs",
    perm_hemoglobinopathies: "Hemoglobinopathies / Red Cell Enzyme Deficiencies with Hemolysis",

    // Step 3 Medication History Table Headers
    med_timeframe: "Timeframe / Duration",
    med_question: "Medication / Condition Question",
    med_answer: "Yes / No",
    yes: "Yes",
    no: "No",

    // Questions 11-17 & Consent Clauses (English)
    q11_endoscopy_title: "11. Endoscopy / Durbeeni Inspection History (दुर्बिणी मधून तपासणी)",
    q11a_endoscopy_sampling: "11A. No sampling done within 7 days?",
    q11b_endoscopy_malignant: "11B (1). Finding is Malignant / Cancer disorder?",
    q11b_endoscopy_benign: "11B (2). Finding is Benign disorder (within 28 days)?",
    q11c_endoscopy_other: "11C. Any other disorder till completion of treatment?",

    q12_blood_donation_title: "12. For Blood Donation History & Past Complications",
    q12a_male_3months: "12A. For males: Have you donated blood in the last 3 months?",
    q12b_female_4months: "12B. For females: Have you donated blood in the last 4 months?",
    q12c_donation_trouble: "12C. Have you faced any trouble/complication after previous blood donations (fainting, swelling, arm discoloration)?",
    q12d_platelets_28days: "12D. Have you donated platelets in the last 28 days (with complete red cell infusion)?",

    q14a_hiv_diagnosis: "14A. Were you diagnosed with HIV/AIDS, Hepatitis B/C, Syphilis, or Gonorrhea?",
    q14b_unsafe_sex: "14B. Are you having unsafe sexual practices (multiple partners / sex for money)?",
    q14c_injected_narcotics: "14C. Have you ever injected drugs/narcotics not prescribed by a qualified doctor?",
    q14d_partner_risk: "14D. Does your sexual partner belong to any above categories (14A, B, C)?",

    q15a_night_sweats: "15A. Night Sweats",
    q15b_persistent_fever: "15B. Persistent Fever",
    q15c_swollen_glands: "15C. Swollen Glands",
    q15d_persistent_diarrhea: "15D. Persistent Diarrhoea",
    q15e_weight_loss: "15E. Unexplained weight loss",

    q16a_female_abortion: "16A. Abortion in the last 6 months?",
    q16b_female_pregnant: "16B. Are you pregnant?",
    q16c_female_delivery: "16C. Delivered a child in the last 12 months?",
    q16d_female_breastfeeding: "16D. Are you breastfeeding your baby?",
    q16e_female_periods: "16E. Are you having your periods today?",
    q16f_female_pcod: "16F. Are you on medication for PCOD?",

    q17a_air_crew: "17A. Role as air crew member?",
    q17b_long_driver: "17B. Driver for long distance vehicle?",
    q17c_strenuous_work: "17C. Strenuous work required?",
    q17d_emergency_service: "17D. Emergency service (Fire / Ambulance)?",
    q17e_altitude_diving: "17E. Work above (flying) or below (diving) sea level?",
    q17f_past_12h_duties: "17F. Performed any of the above duties in the last 12 hours?",

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
    consent_header: "Consent",
    consent_item1: "1) I understand that<br><span style='display:inline-block; margin-left:16px;'>a) Blood donation is a totally voluntary act and no inducement or remuneration has been offered.</span><br><span style='display:inline-block; margin-left:16px;'>b) Donation of blood is a medical procedure and generally not associated with any major risks or side effects. However, I am aware that no medical procedure is without risk and I am voluntarily willing to donate blood.</span><br><span style='display:inline-block; margin-left:16px;'>c) My blood will be tested for Hepatitis B, Hepatitis C, HIV/AIDS, Malaria and Veneral disease in addition to any other screening test required to ensure blood safety.</span>",
    consent_item2: "2) I hereby give consent to utilize my<br><span style='display:inline-block; margin-left:16px;'>a) Plasma component for fractionation</span><br><span style='display:inline-block; margin-left:16px;'>b) Blood and blood component for use of patient beyond the blood centre through blood storage centres and other blood centres.</span>",
    consent_item3: "3) I have read and understood all the information presented and answered all the questions truthfully. Any incorrect statement or concealment may affect my health or may harm the recipient.",
    consent_item4: "4) I prohibit any information about Hepatitis B, Hepatitis C, HIV/AIDS, Malaria and Veneral diseases testing done on my blood to be disclosed to any individual or Government agency without my prior permission.",
    consent_item5: "5) I would like to be informed about any abnormal test result from above mentioned tests.",
    consent_confirm_checkbox: "I hereby agree and confirm all consent declarations.",
    consent_donor_sig_label: "Donor Consent Signature (रक्तदात्याची स्वाक्षरी - Canvas)",
    btn_clear_donor_sig: "Clear Donor Signature",
    consent_yes: "Yes",
    consent_no: "No",
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
    btn_modify: "नोंद बदला",
    btn_edit_user: "संपादित करा",
    btn_change_password: "पासवर्ड बदला",
    btn_delete_user: "हटवा",
    badge_protected_admin: "सुरक्षित प्रशासक",
    title_edit_user: "वापरकर्ता माहिती संपादित करा",
    title_change_password: "वापरकर्ता पासवर्ड बदला",

    // Step Headers
    step_1: "१. रक्तदाता प्राथमिक माहिती",
    step_2: "२. प्राथमिक आरोग्य प्रश्नावली",
    step_3: "३. स्थगिती तक्ता व इतिहास",
    step_4: "४. वैद्यकीय तपासणी (Medical Exam)",
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

    // Table Headers & Controls (Marathi)
    th_no: "क्र.",
    th_question: "प्रश्नावली विधान (मराठी)",
    th_response: "प्रतिसाद",
    opt_yes: "होय",
    opt_no: "नाही",
    med_history_title: "औषधोपचार व आजारांचा इतिहास (कालावधीनुसार स्थगिती तक्ता)",

    // Timeframes (Marathi)
    tf_daily_2m: "दररोज (२ महिने)",
    tf_3days: "गेल्या ३ दिवसांत",
    tf_7days: "गेल्या ७ दिवसांत",
    tf_2weeks: "गेल्या २ आठवड्यांत",
    tf_28days: "गेल्या २८ दिवसांत",
    tf_1month: "गेल्या १ महिन्यात",
    tf_3months: "गेल्या ३ महिन्यात",
    tf_6months: "गेल्या ६ महिन्यात",
    tf_1year: "गेल्या १ वर्षात",
    tf_2years: "गेल्या २ वर्षांत",

    // Medication Descriptions (Marathi)
    med_daily_thyroid_desc: "थायरॉईडच्या कमतरतेसाठी औषधे (Medicines for thyroid disorders)",
    med_3days_aspirin_desc: "ॲस्पिरिन किंवा सॅलिसिलेट्स (Aspirin or Salicylates)",
    med_7days_antifungals_desc: "फंगल संसर्ग किंवा कृमींवरील औषधे (Antifungals / Anthelmintics)",
    med_2weeks_antibiotics_desc: "एंटीबायोटिक्स, स्टिरॉइड्स, कांजिण्या/गोवर, लशी (Pertussis, Hep B, Covid)",
    med_28days_vaccines_desc: "काविळ, टायफॉईड, पोलिओ, डेंग्यू, विषरोधक लस (Anti-tetanus/venom serum)",
    med_1month_acne_prostate_desc: "पिंपल्स/मुहासे औषधोपचार किंवा प्रोस्टेट उपचार (Isotretinoin / Finasteride)",
    med_3months_malaria_desc: "मलेरिया उपचार किंवा किरकोळ शस्त्रक्रिया (Treatment for malaria / Minor Surgery)",
    med_6months_radioactive_desc: "रेडिओॲक्टिव्ह इंजेक्शन, हेअर ट्रान्सप्लांट/PRP, डेंग्यू/चिकुनगुनिया",
    med_1year_rabies_tattoo_desc: "रेबीज लस, काविळ, टॅटू/टोचणे, रक्त संक्रमण/मोठी शस्त्रक्रिया, टायफॉईड",
    med_2years_tb_desc: "क्षयरोग (Tuberculosis) किंवा हाडांचा संसर्ग (Osteomyelitis)",

    // Permanent Deferral Checkboxes (15 - Marathi)
    perm_chest_pain: "छातीत दुखणे / श्वास घेण्यास त्रास / पायांना सूज (Chest Pain / Shortness of Breath)",
    perm_etretinate: "ॲट्रीटिनेट औषध उपचार (Treatment with Etretinate)",
    perm_ankylosing_spondylosis: "अँकायलोझिंग स्पॉन्डिलायसिस (Ankylosing Spondylosis)",
    perm_asthma_lung: "दमा व फुफ्फुसाचा तीव्र आजार (Asthma & Chronic Lung Disease)",
    perm_kidney_disease: "मूत्रपिंडाचा जुनाट संसर्ग / अपयश (Chronic Kidney Infection / Failure)",
    perm_insulin_diabetes: "इन्सुलिनवर आधारित मधुमेह / अवयव गुंतागुंत (Insulin Dependent Diabetes)",
    perm_delayed_faints: "कारण नसताना आलेली मूर्च्छा / दुखापतीसह चक्कर / सलग दोनदा मूर्च्छा",
    perm_epilepsy_fits: "झटके / अपस्मार / मिर्गी (Epilepsy / Fits / Seizures / Convulsions)",
    perm_heart_disease: "हृदयरोग / शस्त्रक्रिया / बायपास / अँजिओप्लास्टी (Heart Disease / Bypass)",
    perm_cancer_cytotoxic: "कर्करोग (Cancer) / किमोथेरपी / स्टेम सेल्स / अवयव प्रत्यारोपण",
    perm_liver_failure: "यकृताचा आजार / कुष्ठरोग / पॉलियुसायथेमिया (Chronic Liver Infection / Leprosy)",
    perm_hiv_high_risk: "एच.आय.व्ही धोका / ट्रान्सजेंडर / एमएसएम / सेक्स वर्कर्स / सिफिलीस / गॉनेरिया",
    perm_severe_allergy: "बेटाडीन / स्पिरीट / बँडेजची तीव्र ॲलर्जी (Severe Allergy to Betadine/Spirit)",
    perm_thyroid_malignant: "थायरॉईड दुर्धर आजार / थायरोटॉक्सिकोसिस / मॅलिग्नंट ट्यूमर",
    perm_hemoglobinopathies: "रक्तपेशी दोष / हिमोग्लोबिन विकार / थॅलेसेमिया (Hemoglobinopathies)",

    // Page 1 Questions (1 to 10) Marathi
    q1_age_18_65: "१. आपण १८-६५ वर्षे या वयोगटातील आहात का ?",
    q2_meals_4h: "२. गेल्या ४ तासांत आपण नाश्ता/जेवण केले आहे का?",
    q3a_slept_well: "३अ. काल रात्री चांगली झोप लागली का?",
    q3b_night_shift_sleep: "३ब. जर आपण रात्रीच्या शिफ्टमध्ये काम करत असाल, तर आपणास पुरेशी शांत झोप मिळाली आहे का?",
    q4_heavy_work_12h: "४. गेल्या १२ तासांत आपण अतिश्रमाची कामे केली आहेत का?",
    q5_malaise_weakness: "५. आज आपणास कणकण /अंगदुखी / अशक्तपणा जाणवत आहे का?",
    q6_cough_cold_mood: "६. आपणास खोकला/सर्दी/डोळे येणे / चिंता/ मूड डिसऑर्डरचा त्रास आहे का?",
    q7_alcohol_24h: "७. गेल्या २४ तासांत आपण मद्य प्राशन केले आहे का?",
    q8_loose_motions_15d: "८. गेल्या १५ दिवसांत आपणास जुलाब / मूत्र संसर्ग/गालगुंड/गोवर/कांजिण्या यांपैकी काही झाले होते का ?",
    q9_migraine_weekly: "९. आपणास आठवड्यातून एकापेक्षा जास्त वेळा मायग्रेन / डोकेदुखीचा त्रास होतो का?",
    q10_daily_meds: "१०. आपण उच्च रक्तदाब, मधुमेह किंवा रक्त पातळ करणाऱ्या औषधांवर आहात का (१ महिन्यात डोस बदललेला नाही)?",
    counselor_name: "रक्तदानपूर्व समुपदेशन करणारे",
    bag_manufacturer: "बॅग उत्पादक (FK/DT/HLL/Maco/TP/JM)",
    collection_duration: "रक्त संकलनाचा कालावधी (मिनिटे)",
    reaction_management: "त्रासाचे निवारण / व्यवस्थापन",

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

    // Questions 11-17 & Consent Clauses (Marathi)
    q11_endoscopy_title: "११. दुर्बिणी मधून तपासणी (Endoscopy History)",
    q11a_endoscopy_sampling: "११A. गेल्या ७ दिवसात नमुना (biopsy) घेतलेला नाही?",
    q11b_endoscopy_malignant: "११B (१). कॅन्सरचे निदान (Malignant disorder) आहे का?",
    q11b_endoscopy_benign: "११B (२). सौम्य आजार निदान (Benign - २८ दिवस) आहे का?",
    q11c_endoscopy_other: "११C. इतर आजारावर उपचार पूर्ण होईपर्यंत?",

    q12_blood_donation_title: "१२. पूर्वीचे रक्तदान व त्रास (Blood Donation History)",
    q12a_male_3months: "१२A. पुरुषांसाठी: गेल्या ३ महिन्यात रक्तदान केले आहे का?",
    q12b_female_4months: "१२B. महिलांसाठी: गेल्या ४ महिन्यात रक्तदान केले आहे का?",
    q12c_donation_trouble: "१२C. मागील रक्तदानानंतर काही त्रास/गुंतागुंत (चक्कर, सूज, हात काळा पडणे) झाली होती का?",
    q12d_platelets_28days: "१२D. गेल्या २८ दिवसांत प्लेटलेट्स दान केले आहेत का?",

    q14a_hiv_diagnosis: "१४A. आपणास एच.आय.व्ही, काविळ (Hep B/C), गुप्तरोग (Syphilis) निदान झाले आहे का?",
    q14b_unsafe_sex: "१४B. असुरक्षित लैंगिक संबंध किंवा अनेक भागीदार आहेत का?",
    q14c_injected_narcotics: "१४C. डॉक्टरांच्या सल्ल्याशिवाय अंमली पदार्थांचे इंजेक्शन घेतले आहे का?",
    q14d_partner_risk: "१४D. आपल्या लैंगिक जोडीदारास वरीलपैकी (१४A, B, C) कोणताही धोका आहे का?",

    q15a_night_sweats: "१५A. रात्री घाम येणे (Night Sweats)",
    q15b_persistent_fever: "१५B. सतत ताप राहणे (Persistent Fever)",
    q15c_swollen_glands: "१५C. लसिका ग्रंथींना सूज (Swollen Glands)",
    q15d_persistent_diarrhea: "१५D. सतत जुलाब होणे (Persistent Diarrhoea)",
    q15e_weight_loss: "१५E. कारण नसताना वजन कमी होणे (Unexplained weight loss)",

    q16a_female_abortion: "१६A. गेल्या ६ महिन्यात गर्भपात झाला आहे का?",
    q16b_female_pregnant: "१६B. आपण गरोदर आहात का?",
    q16c_female_delivery: "१६C. गेल्या १२ महिन्यात प्रसूती झाली आहे का?",
    q16d_female_breastfeeding: "१६D. आपण लहान बाळाला स्तनपान करत आहात का?",
    q16e_female_periods: "१६E. आज आपली मासिक पाळी आहे का?",
    q16f_female_pcod: "१६F. PCOD साठी औषधोपचार चालू आहेत का?",

    q17a_air_crew: "१७A. विमान चालक / विमान क्रू सदस्य म्हणून काम?",
    q17b_long_driver: "१७B. दूरच्या प्रवासाचे वाहन चालक (Driver)?",
    q17c_strenuous_work: "१७C. अतिश्रमाचे काम करावे लागणारे आहे का?",
    q17d_emergency_service: "१७D. आपत्कालीन सेवा (फायर ब्रिगेड / रुग्णवाहिका)?",
    q17e_altitude_diving: "१७E. समुद्राच्या अति उंचावर (उडणे) किंवा खोलवर (डायव्हिंग) काम?",
    q17f_past_12h_duties: "१७F. गेल्या १२ तासांत वरीलपैकी कोणतेही काम केले आहे का?",

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
    consent_header: "मान्यतापत्र",
    consent_item1: "१) मला हे पूर्णपणे समजले आहे की रक्तदान हे पूर्णतः स्वच्छेने करायचे आहे व त्यासाठी मला कोणताही मोबदला देऊ केलेला नाही. रक्त / रक्तघटकांचे दान ही एक वैद्यकीय प्रक्रिया आहे, स्वच्छ रक्तदानातून मी या प्रक्रियेमधील संभाव्य धोके स्विकारत आहे. वरील सर्व माहिती वाचून मी ऐच्छिक रक्तदान करतो / करते आहे. माझ्या रक्तावर कराव्या लागणाऱ्या सर्व प्रकारच्या तपासण्यांची माहिती मला देण्यात आली आहे आणि त्या तपासण्या करण्यास माझी संमती आहे.",
    consent_item2: "२) माझे रक्त / रक्तघटक<br><span style='display:inline-block; margin-left:16px;'>अ) प्लाझ्मा फ्रॅक्शनेशनसाठी वापरण्यास</span><br><span style='display:inline-block; margin-left:16px;'>ब) रक्तपेढीच्या परिक्षेत्राबाहेरील रुग्णांसाठी, रक्तसाठवणूक केंद्रासाठी व अन्य रक्तपेढ्यांमार्फत वापरण्यास मी अनुमती देत आहे.</span>",
    consent_item3: "३) वरील सर्व माहिती वाचून मला समजली आहे. मी सर्व प्रश्नांची उत्तरे विचारपूर्वक, बरोबर दिली आहेत. चुकीची माहिती देणे अथवा कोणतीही माहिती लपवणे याचा माझ्या व रुग्णाच्या आरोग्यावर परिणाम होऊ शकतो याची मला पूर्ण कल्पना आहे.",
    consent_item4: "४) रक्ताच्या सुरक्षिततेसाठी माझ्या रक्तावर एच.आय.व्ही/एड्स, हिपॅटायटीस बी, हिपॅटायटीस सी, सिफिलीस (गुप्तरोग), मलेरीया या तपासण्या केल्या जातील याची कल्पना मला दिली आहे.<br>वरील तपासण्यांचे निदान माझ्या परवानगी शिवाय कोणत्याही व्यक्तीस, संस्थेस किंवा सरकारी यंत्रणेस देण्यात येऊ नये.",
    consent_item5: "५) या तपासण्यांमधील काही तपासण्या दोषपूर्ण आढळल्यास आपल्याला कळवावे का ?<br><small style='color:#64748B;'>होय असल्यास आपणाशी सामाजिक कार्यकर्ते किंवा वैद्यकीय अधिकारी संपर्क करतील.</small>",
    consent_confirm_checkbox: "मी वरील सर्व मान्यतापत्र अटी व शर्ती वाचल्या आहेत आणि त्यास माझी पूर्ण संमती आहे.",
    consent_donor_sig_label: "रक्तदात्याची स्वाक्षरी (Donor Consent Signature - Canvas)",
    btn_clear_donor_sig: "स्वाक्षरी पुसा (Clear)",
    consent_yes: "होय (Yes)",
    consent_no: "नाही (No)",
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
    } else if (el.tagName === 'OPTION') {
      el.textContent = translation;
    } else {
      el.innerHTML = translation;
    }
  });

  // Dynamically update standard Yes / No dropdown options across form steps
  document.querySelectorAll('select option[value="Yes"]').forEach(opt => {
    if (!opt.hasAttribute('data-i18n')) {
      opt.textContent = (currentLang === 'mr') ? 'होय (Yes)' : 'Yes / होय';
    }
  });
  document.querySelectorAll('select option[value="No"]').forEach(opt => {
    if (!opt.hasAttribute('data-i18n')) {
      opt.textContent = (currentLang === 'mr') ? 'नाही (No)' : 'No / नाही';
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

