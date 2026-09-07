-- SQLite Database Schema for Blood Bank System (QF/JKRP/18)

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('ADMIN', 'STAFF', 'MEDICAL_OFFICER')),
    medical_reg_no TEXT,
    signature_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS system_settings (
    setting_key TEXT PRIMARY KEY,
    setting_value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS blood_donation_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_number TEXT UNIQUE NOT NULL,
    donor_number TEXT,
    donation_date DATE NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('DRAFT', 'SUBMITTED', 'MEDICAL_VERIFICATION', 'SIGNED', 'COMPLETED', 'CANCELLED')),
    created_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(created_by) REFERENCES users(id),
    FOREIGN KEY(updated_by) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS donor_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    gender TEXT NOT NULL,
    date_of_birth DATE,
    age INTEGER NOT NULL,
    occupation TEXT,
    organization_company TEXT,
    residential_address TEXT NOT NULL,
    city_district TEXT NOT NULL,
    pincode TEXT,
    mobile_number TEXT NOT NULL,
    email TEXT,
    blood_group_known TEXT,
    donation_type TEXT NOT NULL,
    last_donation_date DATE,
    number_of_past_donations INTEGER DEFAULT 0,
    FOREIGN KEY(record_id) REFERENCES blood_donation_records(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS medical_examinations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER UNIQUE NOT NULL,
    weight_kg REAL NOT NULL,
    height_cm REAL,
    pulse_rate INTEGER NOT NULL,
    bp_systolic INTEGER NOT NULL,
    bp_diastolic INTEGER NOT NULL,
    hemoglobin_g_dl REAL NOT NULL,
    body_temperature REAL NOT NULL,
    skin_site_inspection TEXT NOT NULL,
    screening_outcome TEXT NOT NULL CHECK(screening_outcome IN ('ELIGIBLE', 'DEFERRED', 'REJECTED')),
    deferral_reason TEXT,
    deferral_duration TEXT,
    examined_by_staff_id INTEGER,
    FOREIGN KEY(record_id) REFERENCES blood_donation_records(id) ON DELETE CASCADE,
    FOREIGN KEY(examined_by_staff_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS medication_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER UNIQUE NOT NULL,
    answers_json TEXT NOT NULL,
    FOREIGN KEY(record_id) REFERENCES blood_donation_records(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS permanent_deferrals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER UNIQUE NOT NULL,
    conditions_json TEXT NOT NULL,
    FOREIGN KEY(record_id) REFERENCES blood_donation_records(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS questionnaire_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER UNIQUE NOT NULL,
    answers_json TEXT NOT NULL,
    FOREIGN KEY(record_id) REFERENCES blood_donation_records(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS donor_consent (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER UNIQUE NOT NULL,
    consent_given INTEGER DEFAULT 1,
    abnormal_results_notify INTEGER DEFAULT 1,
    donor_signature_data TEXT,
    consent_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(record_id) REFERENCES blood_donation_records(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS donation_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER UNIQUE NOT NULL,
    blood_bag_number TEXT NOT NULL,
    bag_type TEXT NOT NULL,
    anticoagulant TEXT NOT NULL,
    volume_ml INTEGER NOT NULL,
    segment_number TEXT,
    phlebotomy_site TEXT,
    phlebotomist_staff_id TEXT,
    donation_status TEXT DEFAULT 'SUCCESSFUL',
    adverse_reaction TEXT DEFAULT 'NONE',
    reaction_details TEXT,
    FOREIGN KEY(record_id) REFERENCES blood_donation_records(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS signatures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    user_name TEXT NOT NULL,
    user_role TEXT NOT NULL,
    signature_data TEXT NOT NULL,
    medical_notes TEXT,
    signed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(record_id) REFERENCES blood_donation_records(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT NOT NULL,
    record_id INTEGER,
    record_number TEXT,
    action TEXT NOT NULL,
    details TEXT,
    ip_address TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
