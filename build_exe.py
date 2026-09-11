"""
Automated PyInstaller Build Script for Jankalyan Blood Bank Digital System
==========================================================================
Usage:
    python build_exe.py
"""

import os
import sys
import subprocess
import shutil

def check_and_install_dependencies():
    required_packages = ['flask', 'werkzeug', 'openpyxl', 'waitress', 'pyinstaller']
    missing = []
    
    for pkg in required_packages:
        try:
            __import__(pkg if pkg != 'pyinstaller' else 'PyInstaller')
        except ImportError:
            missing.append(pkg)
            
    if missing:
        print(f"[*] Installing missing build dependencies: {', '.join(missing)} ...")
        cmd = [sys.executable, "-m", "pip", "install"] + missing
        res = subprocess.run(cmd)
        if res.returncode != 0:
            print(f"[!] Failed to install {missing}. Please install manually using: pip install -r requirements.txt")
            sys.exit(1)
        print("[OK] Dependencies installed successfully.")

def clean_previous_builds(base_dir):
    for folder in ['build', 'dist']:
        p = os.path.join(base_dir, folder)
        if os.path.exists(p):
            print(f"[*] Cleaning previous {folder} directory...")
            try:
                shutil.rmtree(p)
            except Exception as e:
                print(f"[!] Warning cleaning {folder}: {e}")

def run_pyinstaller(base_dir):
    spec_path = os.path.join(base_dir, 'bloodbank.spec')
    if not os.path.exists(spec_path):
        print(f"[!] Spec file not found: {spec_path}")
        sys.exit(1)

    print("\n" + "=" * 65)
    print("  Building Jankalyan Blood Bank Standalone Application")
    print("=" * 65)
    print(f"[*] Executing PyInstaller with spec: {spec_path} ...\n")
    
    cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm", spec_path]
    result = subprocess.run(cmd, cwd=base_dir)
    
    if result.returncode == 0:
        dist_dir = os.path.join(base_dir, 'dist', 'JankalyanBloodBank')
        exe_path = os.path.join(dist_dir, 'JankalyanBloodBank.exe')
        print("\n" + "=" * 65)
        print("  BUILD SUCCESSFUL!")
        print("=" * 65)
        print("[OK] Application Directory : " + dist_dir)
        print("[OK] Executable Binary     : " + exe_path)
        print("\nNext Steps:")
        print("1. Test the built executable by running:")
        print(f"   \"{exe_path}\"")
        print("2. Compile the Inno Setup installer script:")
        print("   inno_setup.iss (using Inno Setup Compiler GUI or iscc)")
    else:
        print("\n[!] Build failed. Please check the PyInstaller output above.")
        sys.exit(result.returncode)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    check_and_install_dependencies()
    clean_previous_builds(base_dir)
    run_pyinstaller(base_dir)

if __name__ == '__main__':
    main()
