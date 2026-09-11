"""
Jankalyan Blood Bank Digital System - Standalone Desktop Launcher
=================================================================
This script acts as the main entry point for PyInstaller standalone packaging.
It ensures SQLite database initialization in the writable user data directory,
starts the production WSGI server, and opens the default web browser.
"""

import os
import sys
import time
import socket
import webbrowser
import threading

# Ensure project root is in sys.path
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.path_service import get_db_path, get_data_dir, is_frozen
from database.db_init import init_db
from app import app

def is_port_available(port, host='127.0.0.1'):
    """Check if a local TCP port is available."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False

def find_available_port(start_port=8000, max_attempts=10, host='127.0.0.1'):
    """Find the first available TCP port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        if is_port_available(port, host):
            return port
    return start_port

def open_browser_delayed(url, delay=1.2):
    """Open default web browser after server starts."""
    def _open():
        time.sleep(delay)
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Could not automatically open browser: {e}")
            print(f"Please open your browser manually and visit: {url}")
    threading.Thread(target=_open, daemon=True).start()

def main():
    print("=" * 65)
    print("  Jankalyan Blood Bank Digital System (QF/JKRP/18)")
    print("  Standalone Desktop Application Edition")
    print("=" * 65)
    
    # 1. Ensure SQLite database is present and initialized
    db_path = get_db_path()
    data_dir = get_data_dir()
    print(f"[*] App Data Directory : {data_dir}")
    print(f"[*] SQLite Database    : {db_path}")
    print(f"[*] Frozen Mode (EXE)  : {is_frozen()}")

    if not os.path.exists(db_path):
        print("[+] First run detected. Initializing database schema and default accounts...")
        try:
            init_db(db_path)
            print("[OK] Database initialized successfully.")
        except Exception as e:
            print(f"[!] Database initialization error: {e}")
    else:
        print("[OK] Existing database located.")

    # 2. Determine Host and Port
    host = '127.0.0.1'
    port = find_available_port(8000, 10, host)
    app_url = f"http://{host}:{port}"

    print(f"[*] Starting application server on {app_url} ...")
    print("[*] Launching web browser...")
    open_browser_delayed(app_url)

    # 3. Start Production WSGI Server (Waitress) or Flask fallback
    try:
        from waitress import serve
        print("[OK] WSGI Server: Waitress Production Engine")
        print(f"[OK] Application running. Press Ctrl+C in this console or close the window to exit.")
        print("-" * 65)
        serve(app, host=host, port=port, threads=8, channel_timeout=120)
    except ImportError:
        print("[!] Waitress not found, falling back to Flask server...")
        app.run(host=host, port=port, debug=False)
    except (KeyboardInterrupt, SystemExit):
        print("\n[*] Server shutdown requested. Exiting cleanly...")

if __name__ == '__main__':
    main()
