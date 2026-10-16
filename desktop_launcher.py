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

def is_port_available(port, host='0.0.0.0'):
    """Check if a TCP port is available on the specified interface."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False

def find_available_port(start_port=8000, max_attempts=10, host='0.0.0.0'):
    """Find the first available TCP port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        if is_port_available(port, host):
            return port
    return start_port

def get_wifi_lan_ips():
    """Retrieve all non-loopback IPv4 addresses assigned to active network adapters (Wi-Fi/LAN)."""
    ip_list = []
    # Primary outbound route detection (most accurate for active Wi-Fi / LAN connection)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(('8.8.8.8', 80))
        primary_ip = s.getsockname()[0]
        s.close()
        if primary_ip and not primary_ip.startswith('127.'):
            ip_list.append(primary_ip)
    except Exception:
        pass

    # Secondary lookup via hostname resolution
    try:
        hostname = socket.gethostname()
        for item in socket.getaddrinfo(hostname, None):
            ip = item[4][0]
            if ':' not in ip and not ip.startswith('127.') and ip not in ip_list:
                ip_list.append(ip)
    except Exception:
        pass

    return ip_list

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

    # 2. Determine Host, Network IPs, and Port
    # Listen on 0.0.0.0 so all network interfaces (Wi-Fi, LAN, Localhost) are accessible
    bind_host = '0.0.0.0'
    port = find_available_port(8000, 10, bind_host)
    local_url = f"http://127.0.0.1:{port}"
    network_ips = get_wifi_lan_ips()

    print("\n" + "=" * 65)
    print("  SERVER ACCESS ADDRESSES (LOCAL & WI-FI / LAN NETWORK)")
    print("=" * 65)
    print(f"  [This PC Local Access]  : {local_url}")
    
    if network_ips:
        print("  [Wi-Fi / LAN Access for Other Devices (Tablets/Mobiles/PCs)]:")
        for ip in network_ips:
            print(f"   ---> http://{ip}:{port}")
    else:
        print("  [Wi-Fi / LAN Access]    : No active Wi-Fi/Ethernet IP detected.")
        print("                            Connect to Wi-Fi to allow other devices to access.")
    
    print("-" * 65)
    print("  [FIREWALL NOTICE]: If other devices on Wi-Fi cannot connect,")
    print("  ensure Windows Firewall allows Port 8000 (or JankalyanBloodBank.exe).")
    print("=" * 65 + "\n")

    print("[*] Launching local web browser...")
    open_browser_delayed(local_url)

    # 3. Start Production WSGI Server (Waitress) or Flask fallback
    try:
        from waitress import serve
        print("[OK] WSGI Server: Waitress Production Engine running on 0.0.0.0")
        print(f"[OK] Application active. Press Ctrl+C or close console to stop.\n")
        serve(app, host=bind_host, port=port, threads=8, channel_timeout=120)
    except ImportError:
        print("[!] Waitress not found, falling back to Flask server...")
        app.run(host=bind_host, port=port, debug=False)
    except (KeyboardInterrupt, SystemExit):
        print("\n[*] Server shutdown requested. Exiting cleanly...")

if __name__ == '__main__':
    main()
