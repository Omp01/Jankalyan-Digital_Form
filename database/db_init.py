import os
import sys
import sqlite3
from werkzeug.security import generate_password_hash

# Ensure project root is in sys.path when running db_init.py directly
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from services.path_service import get_db_path, get_resource_path

def get_schema_path():
    # Look for schema.sql in resource path or local folder
    res_path = get_resource_path(os.path.join('database', 'schema.sql'))
    if os.path.exists(res_path):
        return res_path
    local_path = os.path.join(current_dir, 'schema.sql')
    return local_path

def init_db(target_db_path=None):
    db_path = target_db_path or get_db_path()
    schema_path = get_schema_path()
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    print(f"Initializing SQLite database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Read and execute schema
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)

    # Migration check for signature_data and is_active columns in users table
    cursor.execute("PRAGMA table_info(users)")
    cols = [column[1] for column in cursor.fetchall()]
    if 'signature_data' not in cols:
        print("Migrating users table: adding signature_data column...")
        cursor.execute("ALTER TABLE users ADD COLUMN signature_data TEXT")
    if 'is_active' not in cols:
        print("Migrating users table: adding is_active column...")
        cursor.execute("ALTER TABLE users ADD COLUMN is_active INTEGER DEFAULT 1")
        cursor.execute("UPDATE users SET is_active = 1 WHERE is_active IS NULL")

    # Seed Default Users if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    if user_count == 0:
        print("Seeding initial users...")
        users_data = [
            ('admin', generate_password_hash('Admin@123'), 'System Administrator', 'ADMIN', 'ADMIN-001', None),
            ('staff', generate_password_hash('Staff@123'), 'Blood Bank Staff Person', 'STAFF', 'STF-101', None),
            ('doctor', generate_password_hash('Doctor@123'), 'Dr. Rajesh Sharma (Medical Officer)', 'MEDICAL_OFFICER', 'MMC-2024-88990', None)
        ]
        cursor.executemany("""
            INSERT INTO users (username, password_hash, full_name, role, medical_reg_no, signature_data)
            VALUES (?, ?, ?, ?, ?, ?)
        """, users_data)

    # Seed System Settings if empty
    default_settings = [
        ('record_prefix', 'BB'),
        ('record_seq', '1'),
        ('hospital_name', 'Jankalyan Blood Centre & Hospital'),
        ('hospital_address', 'Pune, Maharashtra')
    ]
    for key, val in default_settings:
        cursor.execute("INSERT OR IGNORE INTO system_settings (setting_key, setting_value) VALUES (?, ?)", (key, val))

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
