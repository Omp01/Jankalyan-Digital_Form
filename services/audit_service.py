from services.db_service import execute_db
from flask import request, session

def log_audit(action, record_id=None, record_number=None, details=None):
    try:
        user_id = session.get('user_id')
        username = session.get('username', 'ANONYMOUS')
        ip_address = request.remote_addr if request else '127.0.0.1'

        execute_db("""
            INSERT INTO audit_logs (user_id, username, record_id, record_number, action, details, ip_address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, username, record_id, record_number, action, details, ip_address))
    except Exception as e:
        print(f"Error logging audit: {e}")
