import os
import sqlite3
from flask import g

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'bloodbank.db')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        # Enable foreign keys
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    last_id = cur.lastrowid
    cur.close()
    return last_id

def generate_record_number():
    db = get_db()
    cur = db.execute("SELECT setting_value FROM system_settings WHERE setting_key = 'record_prefix'")
    row = cur.fetchone()
    prefix = row['setting_value'] if row else 'BB'

    cur = db.execute("SELECT setting_value FROM system_settings WHERE setting_key = 'record_seq'")
    row = cur.fetchone()
    seq = int(row['setting_value']) if row else 1

    import datetime
    current_year = datetime.datetime.now().year
    rec_num = f"{prefix}-{current_year}-{seq:06d}"

    # Increment sequence for next record
    db.execute("UPDATE system_settings SET setting_value = ? WHERE setting_key = 'record_seq'", (str(seq + 1),))
    db.commit()

    return rec_num
