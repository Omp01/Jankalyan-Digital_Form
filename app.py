import os
import json
import sqlite3
import datetime
from flask import Flask, request, jsonify, render_template, send_file, session, redirect, url_for, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from services.db_service import get_db, close_db, query_db, execute_db, generate_record_number, DB_PATH
from services.audit_service import log_audit
from services.excel_service import generate_records_excel
from middleware.auth_decorator import login_required, roles_required

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'blood_bank_super_secret_session_key_hospital_2026'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=12)

def to_db_date(val):
    """Converts DD-MM-YYYY or YYYY-MM-DD to YYYY-MM-DD for DB storage."""
    if not val:
        return None
    val = str(val).strip()
    if not val:
        return None
    parts = val.split('-')
    if len(parts) == 3:
        if len(parts[0]) == 2 and len(parts[2]) == 4: # DD-MM-YYYY
            return f"{parts[2]}-{parts[1]}-{parts[0]}"
        elif len(parts[0]) == 4 and len(parts[2]) == 2: # YYYY-MM-DD
            return val
    return val

def to_display_date(val):
    """Converts YYYY-MM-DD or ISO datetime to DD-MM-YYYY [HH:MM:SS]."""
    if not val:
        return ''
    val = str(val).strip()
    if not val or val == 'N/A' or val == 'None':
        return val
    if ' ' in val or 'T' in val:
        parts = val.replace('T', ' ').split(' ')
        d_part = parts[0]
        t_part = ' '.join(parts[1:])
        dp = d_part.split('-')
        if len(dp) == 3 and len(dp[0]) == 4: # YYYY-MM-DD
            return f"{dp[2]}-{dp[1]}-{dp[0]} {t_part}".strip()
        elif len(dp) == 3 and len(dp[0]) == 2: # DD-MM-YYYY
            return val
        return val
    dp = val.split('-')
    if len(dp) == 3 and len(dp[0]) == 4: # YYYY-MM-DD
        return f"{dp[2]}-{dp[1]}-{dp[0]}"
    return val

@app.template_filter('format_date')
def jinja_format_date(val):
    return to_display_date(val)

@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

# ==================== STATIC FILE ROUTING ====================
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard.html')
    return redirect('/login.html')

@app.route('/<path:filename>')
def serve_static(filename):
    static_file = os.path.join(app.static_folder, filename)
    if os.path.isfile(static_file):
        return send_from_directory(app.static_folder, filename)
    return jsonify({'error': 'Page not found'}), 404

# ==================== AUTHENTICATION APIs ====================
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required'}), 400

    user = query_db("SELECT * FROM users WHERE username = ?", (username,), one=True)
    if not user or not check_password_hash(user['password_hash'], password):
        log_audit('LOGIN_FAILED', details=f"Attempted username: {username}")
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

    session.permanent = True
    session['user_id'] = user['id']
    session['username'] = user['username']
    session['full_name'] = user['full_name']
    session['role'] = user['role']

    log_audit('LOGIN', details=f"Logged in as {user['role']}")
    return jsonify({
        'success': True,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'full_name': user['full_name'],
            'role': user['role'],
            'medical_reg_no': user['medical_reg_no']
        }
    })

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    log_audit('LOGOUT')
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/auth/me', methods=['GET'])
def api_me():
    if 'user_id' not in session:
        return jsonify({'logged_in': False})
    
    user = query_db("SELECT id, username, full_name, role, medical_reg_no, signature_data FROM users WHERE id = ?", (session.get('user_id'),), one=True)
    return jsonify({
        'logged_in': True,
        'user': dict(user) if user else {
            'id': session.get('user_id'),
            'username': session.get('username'),
            'full_name': session.get('full_name'),
            'role': session.get('role')
        }
    })

@app.route('/api/profile', methods=['GET'])
@login_required
def get_profile():
    user_id = session.get('user_id')
    user = query_db("SELECT id, username, full_name, role, medical_reg_no, signature_data FROM users WHERE id = ?", (user_id,), one=True)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    return jsonify({'success': True, 'profile': dict(user)})

@app.route('/api/profile/signature', methods=['POST'])
@login_required
def update_profile_signature():
    data = request.get_json() or {}
    signature_data = data.get('signature_data', '').strip()
    if not signature_data:
        return jsonify({'success': False, 'message': 'Signature data is required'}), 400

    user_id = session.get('user_id')
    execute_db("UPDATE users SET signature_data = ? WHERE id = ?", (signature_data, user_id))
    log_audit('PROFILE_SIGNATURE_UPDATED', details=f"User {session.get('username')} updated profile signature")
    return jsonify({'success': True, 'message': 'Digital signature saved to profile successfully.'})

# ==================== USER MANAGEMENT APIs (ADMIN ONLY) ====================
@app.route('/api/users', methods=['GET'])
@roles_required(['ADMIN'])
def get_users():
    users = query_db("SELECT id, username, full_name, role, medical_reg_no, created_at FROM users ORDER BY id DESC")
    out = []
    for u in users:
        u_dict = dict(u)
        u_dict['created_at'] = to_display_date(u_dict.get('created_at'))
        out.append(u_dict)
    return jsonify({'success': True, 'users': out})

@app.route('/api/users', methods=['POST'])
@roles_required(['ADMIN'])
def create_user():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    full_name = data.get('full_name', '').strip()
    role = data.get('role', 'STAFF')
    medical_reg_no = data.get('medical_reg_no', '').strip()

    if not username or not password or not full_name:
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400

    if role not in ['ADMIN', 'STAFF', 'MEDICAL_OFFICER']:
        return jsonify({'success': False, 'message': 'Invalid role'}), 400

    existing = query_db("SELECT id FROM users WHERE username = ?", (username,), one=True)
    if existing:
        return jsonify({'success': False, 'message': 'Username already exists'}), 400

    pwd_hash = generate_password_hash(password)
    user_id = execute_db("""
        INSERT INTO users (username, password_hash, full_name, role, medical_reg_no)
        VALUES (?, ?, ?, ?, ?)
    """, (username, pwd_hash, full_name, role, medical_reg_no))

    log_audit('USER_CREATED', details=f"Created user {username} with role {role}")
    return jsonify({'success': True, 'user_id': user_id, 'message': 'User created successfully'})

# ==================== RECORD MANAGEMENT APIs ====================
@app.route('/api/records', methods=['GET'])
@login_required
def get_records():
    search = request.args.get('search', '').strip()
    status = request.args.get('status', '').strip()
    blood_group = request.args.get('blood_group', '').strip()
    from_date = request.args.get('from_date', '').strip()
    to_date = request.args.get('to_date', '').strip()

    query = """
        SELECT r.id, r.record_number, r.donor_number, r.donation_date, r.status, r.created_at,
               d.full_name, d.gender, d.age, d.mobile_number, d.city_district, d.blood_group_known, d.donation_type,
               m.screening_outcome, b.blood_bag_number, b.bag_type, b.volume_ml,
               u1.full_name as created_by_name, u2.user_name as signed_by_name
        FROM blood_donation_records r
        LEFT JOIN donor_details d ON r.id = d.record_id
        LEFT JOIN medical_examinations m ON r.id = m.record_id
        LEFT JOIN donation_details b ON r.id = b.record_id
        LEFT JOIN users u1 ON r.created_by = u1.id
        LEFT JOIN signatures u2 ON r.id = u2.record_id
        WHERE 1=1
    """
    params = []

    if search:
        query += " AND (r.record_number LIKE ? OR r.donor_number LIKE ? OR d.full_name LIKE ? OR d.mobile_number LIKE ? OR b.blood_bag_number LIKE ?)"
        pattern = f"%{search}%"
        params.extend([pattern, pattern, pattern, pattern, pattern])

    if status:
        query += " AND r.status = ?"
        params.append(status)

    if blood_group:
        query += " AND d.blood_group_known = ?"
        params.append(blood_group)

    if from_date:
        query += " AND r.donation_date >= ?"
        params.append(to_db_date(from_date))

    if to_date:
        query += " AND r.donation_date <= ?"
        params.append(to_db_date(to_date))

    query += " ORDER BY r.id DESC"
    records = query_db(query, params)
    out = []
    for r in records:
        r_dict = dict(r)
        r_dict['donation_date'] = to_display_date(r_dict.get('donation_date'))
        r_dict['created_at'] = to_display_date(r_dict.get('created_at'))
        out.append(r_dict)
    return jsonify({'success': True, 'records': out})

@app.route('/api/records/<int:record_id>', methods=['GET'])
@login_required
def get_record(record_id):
    rec = query_db("SELECT * FROM blood_donation_records WHERE id = ?", (record_id,), one=True)
    if not rec:
        return jsonify({'success': False, 'message': 'Record not found'}), 404

    donor = query_db("SELECT * FROM donor_details WHERE record_id = ?", (record_id,), one=True)
    med_exam = query_db("SELECT * FROM medical_examinations WHERE record_id = ?", (record_id,), one=True)
    med_hist = query_db("SELECT * FROM medication_history WHERE record_id = ?", (record_id,), one=True)
    perm_def = query_db("SELECT * FROM permanent_deferrals WHERE record_id = ?", (record_id,), one=True)
    quest = query_db("SELECT * FROM questionnaire_answers WHERE record_id = ?", (record_id,), one=True)
    consent = query_db("SELECT * FROM donor_consent WHERE record_id = ?", (record_id,), one=True)
    donation = query_db("SELECT * FROM donation_details WHERE record_id = ?", (record_id,), one=True)
    signature = query_db("SELECT * FROM signatures WHERE record_id = ?", (record_id,), one=True)

    rec_dict = dict(rec)
    rec_dict['donation_date'] = to_display_date(rec_dict.get('donation_date'))
    rec_dict['created_at'] = to_display_date(rec_dict.get('created_at'))
    rec_dict['updated_at'] = to_display_date(rec_dict.get('updated_at'))

    donor_dict = dict(donor) if donor else {}
    if donor_dict.get('date_of_birth'):
        donor_dict['date_of_birth'] = to_display_date(donor_dict.get('date_of_birth'))
    if donor_dict.get('last_donation_date'):
        donor_dict['last_donation_date'] = to_display_date(donor_dict.get('last_donation_date'))

    sig_dict = dict(signature) if signature else {}
    if sig_dict.get('signed_at'):
        sig_dict['signed_at'] = to_display_date(sig_dict.get('signed_at'))

    return jsonify({
        'success': True,
        'record': rec_dict,
        'donor': donor_dict,
        'medical_exam': dict(med_exam) if med_exam else {},
        'medication_history': json.loads(med_hist['answers_json']) if med_hist else {},
        'permanent_deferrals': json.loads(perm_def['conditions_json']) if perm_def else [],
        'questionnaire_answers': json.loads(quest['answers_json']) if quest else {},
        'consent': dict(consent) if consent else {},
        'donation_details': dict(donation) if donation else {},
        'signature': sig_dict
    })

@app.route('/api/records', methods=['POST'])
@login_required
def create_or_update_record():
    data = request.get_json() or {}
    record_id = data.get('record_id')
    save_as_draft = data.get('save_as_draft', True)

    donor = data.get('donor', {})
    med_exam = data.get('medical_exam', {})
    med_hist = data.get('medication_history', {})
    perm_def = data.get('permanent_deferrals', [])
    quest = data.get('questionnaire_answers', {})
    consent = data.get('consent', {})
    donation = data.get('donation_details', {})

    user_id = session.get('user_id')

    if record_id:
        existing = query_db("SELECT status FROM blood_donation_records WHERE id = ?", (record_id,), one=True)
        if not existing:
            return jsonify({'success': False, 'message': 'Record not found'}), 404
        if existing['status'] in ['SIGNED', 'COMPLETED'] and session.get('role') != 'ADMIN':
            return jsonify({'success': False, 'message': 'Record is finalized and locked. Editing is not permitted.'}), 403

        status = 'DRAFT' if save_as_draft else 'SUBMITTED'
        donation_date_db = to_db_date(donor.get('donation_date'))
        if donation_date_db:
            execute_db("UPDATE blood_donation_records SET updated_by = ?, updated_at = CURRENT_TIMESTAMP, status = ?, donation_date = ? WHERE id = ?",
                       (user_id, status, donation_date_db, record_id))
        else:
            execute_db("UPDATE blood_donation_records SET updated_by = ?, updated_at = CURRENT_TIMESTAMP, status = ? WHERE id = ?",
                       (user_id, status, record_id))
    else:
        rec_num = generate_record_number()
        donation_date = to_db_date(donor.get('donation_date')) or datetime.date.today().isoformat()
        status = 'DRAFT' if save_as_draft else 'SUBMITTED'
        record_id = execute_db("""
            INSERT INTO blood_donation_records (record_number, donor_number, donation_date, status, created_by)
            VALUES (?, ?, ?, ?, ?)
        """, (rec_num, donor.get('donor_number', ''), donation_date, status, user_id))

    rec = query_db("SELECT record_number FROM blood_donation_records WHERE id = ?", (record_id,), one=True)
    rec_num = rec['record_number']

    dob_db = to_db_date(donor.get('date_of_birth'))
    last_don_db = to_db_date(donor.get('last_donation_date'))

    execute_db("DELETE FROM donor_details WHERE record_id = ?", (record_id,))
    execute_db("""
        INSERT INTO donor_details (record_id, full_name, gender, date_of_birth, age, occupation, organization_company,
                                  residential_address, city_district, pincode, mobile_number, email, blood_group_known,
                                  donation_type, last_donation_date, number_of_past_donations)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record_id, donor.get('full_name', ''), donor.get('gender', 'Male'), dob_db,
        int(donor.get('age', 18)), donor.get('occupation', ''), donor.get('organization_company', ''),
        donor.get('residential_address', ''), donor.get('city_district', ''), donor.get('pincode', ''),
        donor.get('mobile_number', ''), donor.get('email', ''), donor.get('blood_group_known', 'Unknown'),
        donor.get('donation_type', 'Voluntary'), last_don_db, int(donor.get('number_of_past_donations', 0))
    ))

    execute_db("DELETE FROM medical_examinations WHERE record_id = ?", (record_id,))
    execute_db("""
        INSERT INTO medical_examinations (record_id, weight_kg, height_cm, pulse_rate, bp_systolic, bp_diastolic,
                                           hemoglobin_g_dl, body_temperature, skin_site_inspection, screening_outcome,
                                           deferral_reason, deferral_duration, examined_by_staff_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record_id, float(med_exam.get('weight_kg', 50)), float(med_exam.get('height_cm', 165)) if med_exam.get('height_cm') else None,
        int(med_exam.get('pulse_rate', 72)), int(med_exam.get('bp_systolic', 120)), int(med_exam.get('bp_diastolic', 80)),
        float(med_exam.get('hemoglobin_g_dl', 13.5)), float(med_exam.get('body_temperature', 98.6)),
        med_exam.get('skin_site_inspection', 'Satisfactory'), med_exam.get('screening_outcome', 'ELIGIBLE'),
        med_exam.get('deferral_reason', ''), med_exam.get('deferral_duration', ''), user_id
    ))

    execute_db("DELETE FROM medication_history WHERE record_id = ?", (record_id,))
    execute_db("INSERT INTO medication_history (record_id, answers_json) VALUES (?, ?)", (record_id, json.dumps(med_hist)))

    execute_db("DELETE FROM permanent_deferrals WHERE record_id = ?", (record_id,))
    execute_db("INSERT INTO permanent_deferrals (record_id, conditions_json) VALUES (?, ?)", (record_id, json.dumps(perm_def)))

    execute_db("DELETE FROM questionnaire_answers WHERE record_id = ?", (record_id,))
    execute_db("INSERT INTO questionnaire_answers (record_id, answers_json) VALUES (?, ?)", (record_id, json.dumps(quest)))

    execute_db("DELETE FROM donor_consent WHERE record_id = ?", (record_id,))
    execute_db("""
        INSERT INTO donor_consent (record_id, consent_given, abnormal_results_notify, donor_signature_data)
        VALUES (?, ?, ?, ?)
    """, (record_id, 1 if consent.get('consent_given', True) else 0, 1 if consent.get('abnormal_results_notify', True) else 0, consent.get('donor_signature_data', '')))

    execute_db("DELETE FROM donation_details WHERE record_id = ?", (record_id,))
    execute_db("""
        INSERT INTO donation_details (record_id, blood_bag_number, bag_type, anticoagulant, volume_ml, segment_number,
                                       phlebotomy_site, phlebotomist_staff_id, donation_status, adverse_reaction, reaction_details)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record_id, donation.get('blood_bag_number', f"BAG-{record_id}"), donation.get('bag_type', 'Single'),
        donation.get('anticoagulant', 'CPDA-1'), int(donation.get('volume_ml', 350)), donation.get('segment_number', ''),
        donation.get('phlebotomy_site', 'Right Arm'), donation.get('phlebotomist_staff_id', session.get('full_name')),
        donation.get('donation_status', 'SUCCESSFUL'), donation.get('adverse_reaction', 'NONE'), donation.get('reaction_details', '')
    ))

    action = 'RECORD_UPDATED' if data.get('record_id') else 'RECORD_CREATED'
    log_audit(action, record_id=record_id, record_number=rec_num, details=f"Status: {status}")

    return jsonify({
        'success': True,
        'record_id': record_id,
        'record_number': rec_num,
        'status': status,
        'message': f"Record {rec_num} saved successfully as {status}."
    })

@app.route('/api/records/<int:record_id>/submit', methods=['POST'])
@roles_required(['STAFF', 'ADMIN'])
def submit_record(record_id):
    rec = query_db("SELECT record_number, status FROM blood_donation_records WHERE id = ?", (record_id,), one=True)
    if not rec:
        return jsonify({'success': False, 'message': 'Record not found'}), 404

    execute_db("UPDATE blood_donation_records SET status = 'MEDICAL_VERIFICATION' WHERE id = ?", (record_id,))
    log_audit('RECORD_SUBMITTED', record_id=record_id, record_number=rec['record_number'], details="Submitted for Medical Verification")
    return jsonify({'success': True, 'message': f"Record {rec['record_number']} submitted for Medical Verification."})

@app.route('/api/records/<int:record_id>/sign', methods=['POST'])
@roles_required(['MEDICAL_OFFICER', 'ADMIN'])
def sign_record(record_id):
    data = request.get_json() or {}
    signature_data = data.get('signature_data', '').strip()
    medical_notes = data.get('medical_notes', '').strip()

    if not signature_data:
        return jsonify({'success': False, 'message': 'Signature canvas image data is required'}), 400

    rec = query_db("SELECT record_number, status FROM blood_donation_records WHERE id = ?", (record_id,), one=True)
    if not rec:
        return jsonify({'success': False, 'message': 'Record not found'}), 404

    user_id = session.get('user_id')
    user_name = session.get('full_name')
    user_role = session.get('role')

    execute_db("DELETE FROM signatures WHERE record_id = ?", (record_id,))
    execute_db("""
        INSERT INTO signatures (record_id, user_id, user_name, user_role, signature_data, medical_notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (record_id, user_id, user_name, user_role, signature_data, medical_notes))

    execute_db("UPDATE blood_donation_records SET status = 'SIGNED', updated_by = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (user_id, record_id))

    log_audit('SIGNATURE_ADDED', record_id=record_id, record_number=rec['record_number'], details=f"Signed by Medical Officer {user_name}")
    log_audit('RECORD_FINALISED', record_id=record_id, record_number=rec['record_number'], details="Record locked and completed")

    return jsonify({'success': True, 'message': f"Record {rec['record_number']} successfully verified, signed, and locked."})

@app.route('/api/records/<int:record_id>/unlock', methods=['POST'])
@roles_required(['ADMIN', 'MEDICAL_OFFICER'])
def unlock_record(record_id):
    data = request.get_json() or {}
    reason = data.get('reason', '').strip()
    if not reason:
        return jsonify({'success': False, 'message': 'Reason for unlocking record is required'}), 400

    rec = query_db("SELECT record_number FROM blood_donation_records WHERE id = ?", (record_id,), one=True)
    if not rec:
        return jsonify({'success': False, 'message': 'Record not found'}), 404

    execute_db("UPDATE blood_donation_records SET status = 'DRAFT' WHERE id = ?", (record_id,))
    log_audit('RECORD_UNLOCKED', record_id=record_id, record_number=rec['record_number'], details=f"Unlocked for modification. Reason: {reason}")
    return jsonify({'success': True, 'message': f"Record {rec['record_number']} unlocked for authorized changes."})

# ==================== A4 PRINTING TEMPLATE ROUTE ====================
@app.route('/print/<int:record_id>')
@login_required
def print_record(record_id):
    rec = query_db("SELECT * FROM blood_donation_records WHERE id = ?", (record_id,), one=True)
    if not rec:
        return "Record Not Found", 404

    donor = query_db("SELECT * FROM donor_details WHERE record_id = ?", (record_id,), one=True)
    med_exam = query_db("SELECT * FROM medical_examinations WHERE record_id = ?", (record_id,), one=True)
    med_hist = query_db("SELECT * FROM medication_history WHERE record_id = ?", (record_id,), one=True)
    perm_def = query_db("SELECT * FROM permanent_deferrals WHERE record_id = ?", (record_id,), one=True)
    quest = query_db("SELECT * FROM questionnaire_answers WHERE record_id = ?", (record_id,), one=True)
    consent = query_db("SELECT * FROM donor_consent WHERE record_id = ?", (record_id,), one=True)
    donation = query_db("SELECT * FROM donation_details WHERE record_id = ?", (record_id,), one=True)
    signature = query_db("SELECT * FROM signatures WHERE record_id = ?", (record_id,), one=True)

    log_audit('RECORD_PRINTED', record_id=record_id, record_number=rec['record_number'])

    return render_template(
        'print_form.html',
        record=dict(rec),
        donor=dict(donor) if donor else {},
        medical_exam=dict(med_exam) if med_exam else {},
        medication_history=json.loads(med_hist['answers_json']) if med_hist else {},
        permanent_deferrals=json.loads(perm_def['conditions_json']) if perm_def else [],
        questionnaire_answers=json.loads(quest['answers_json']) if quest else {},
        consent=dict(consent) if consent else {},
        donation=dict(donation) if donation else {},
        signature=dict(signature) if signature else {}
    )

# ==================== EXCEL EXPORT API ====================
@app.route('/api/export/excel', methods=['GET'])
@roles_required(['ADMIN', 'STAFF', 'MEDICAL_OFFICER'])
def export_excel():
    search = request.args.get('search', '').strip()
    status = request.args.get('status', '').strip()
    blood_group = request.args.get('blood_group', '').strip()
    from_date = request.args.get('from_date', '').strip()
    to_date = request.args.get('to_date', '').strip()

    query = """
        SELECT r.record_number, r.donation_date, r.status,
               d.full_name, d.gender, d.age, d.mobile_number, d.city_district, d.blood_group_known, d.donation_type,
               m.weight_kg, m.bp_systolic, m.bp_diastolic, m.hemoglobin_g_dl, m.screening_outcome,
               b.blood_bag_number, b.bag_type, b.volume_ml,
               u1.full_name as created_by_name, u2.user_name as signed_by_name
        FROM blood_donation_records r
        LEFT JOIN donor_details d ON r.id = d.record_id
        LEFT JOIN medical_examinations m ON r.id = m.record_id
        LEFT JOIN donation_details b ON r.id = b.record_id
        LEFT JOIN users u1 ON r.created_by = u1.id
        LEFT JOIN signatures u2 ON r.id = u2.record_id
        WHERE 1=1
    """
    params = []

    if search:
        query += " AND (r.record_number LIKE ? OR d.full_name LIKE ? OR b.blood_bag_number LIKE ?)"
        pattern = f"%{search}%"
        params.extend([pattern, pattern, pattern])

    if status:
        query += " AND r.status = ?"
        params.append(status)

    if blood_group:
        query += " AND d.blood_group_known = ?"
        params.append(blood_group)

    if from_date:
        query += " AND r.donation_date >= ?"
        params.append(to_db_date(from_date))

    if to_date:
        query += " AND r.donation_date <= ?"
        params.append(to_db_date(to_date))

    query += " ORDER BY r.id DESC"
    records = [dict(r) for r in query_db(query, params)]
    for r in records:
        r['donation_date'] = to_display_date(r.get('donation_date'))

    excel_file = generate_records_excel(records)
    log_audit('EXCEL_EXPORTED', details=f"Exported {len(records)} records")

    return send_file(
        excel_file,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'BloodBank_Records_{datetime.date.today().isoformat()}.xlsx'
    )

# ==================== DATABASE BACKUP & RESTORE APIs ====================
@app.route('/api/backup/download', methods=['GET'])
@roles_required(['ADMIN'])
def download_backup():
    if not os.path.exists(DB_PATH):
        return jsonify({'success': False, 'message': 'Database file not found'}), 404

    log_audit('DATABASE_BACKUP', details="Admin downloaded bloodbank.db backup")
    backup_filename = f"bloodbank_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    return send_file(DB_PATH, as_attachment=True, download_name=backup_filename)

@app.route('/api/backup/restore', methods=['POST'])
@roles_required(['ADMIN'])
def restore_backup():
    if 'backup_file' not in request.files:
        return jsonify({'success': False, 'message': 'No backup file uploaded'}), 400

    file = request.files['backup_file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400

    if not file.filename.endswith('.db'):
        return jsonify({'success': False, 'message': 'Invalid file format. Must be a .db file.'}), 400

    close_db()
    file.save(DB_PATH)

    log_audit('DATABASE_RESTORED', details=f"Database restored from {file.filename}")
    return jsonify({'success': True, 'message': 'Database restored successfully.'})

# ==================== AUDIT LOGS API ====================
@app.route('/api/audit-logs', methods=['GET'])
@roles_required(['ADMIN'])
def get_audit_logs():
    logs = query_db("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 200")
    out = []
    for l in logs:
        l_dict = dict(l)
        l_dict['timestamp'] = to_display_date(l_dict.get('timestamp'))
        out.append(l_dict)
    return jsonify({'success': True, 'logs': out})

if __name__ == '__main__':
    print("Starting Jankalyan Blood Bank Digital Form System server on http://localhost:5000 ...")
    app.run(host='0.0.0.0', port=5000, debug=False)
