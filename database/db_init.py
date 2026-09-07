import os
import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'bloodbank.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def init_db():
    print(f"Initializing SQLite database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Read and execute schema
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)

    # Seed Default Users if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    if user_count == 0:
        print("Seeding initial users...")
        users_data = [
            ('admin', generate_password_hash('Admin@123'), 'System Administrator', 'ADMIN', 'ADMIN-001'),
            ('staff', generate_password_hash('Staff@123'), 'Blood Bank Staff Person', 'STAFF', 'STF-101'),
            ('doctor', generate_password_hash('Doctor@123'), 'Dr. Rajesh Sharma (Medical Officer)', 'MEDICAL_OFFICER', 'MMC-2024-88990')
        ]
        cursor.executemany("""
            INSERT INTO users (username, password_hash, full_name, role, medical_reg_no)
            VALUES (?, ?, ?, ?, ?)
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
