import os
import sys

def is_frozen():
    """Check if the application is running in a PyInstaller bundle."""
    return getattr(sys, 'frozen', False)

def get_base_dir():
    """
    Get the base directory where read-only bundled application files (templates, static, schema) reside.
    When running in PyInstaller, this points to sys._MEIPASS (onefile) or sys.executable dir (onedir).
    When running directly in Python, this points to the repository root directory.
    """
    if is_frozen():
        if hasattr(sys, '_MEIPASS'):
            return sys._MEIPASS
        return os.path.dirname(sys.executable)
    # 2 levels up from services/path_service.py -> project root
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_resource_path(relative_path):
    """
    Get the absolute path to a read-only bundled resource (templates, static, schema.sql, etc.).
    """
    base = get_base_dir()
    return os.path.normpath(os.path.join(base, relative_path))

def get_data_dir():
    """
    Get the directory where writable runtime data (SQLite database, backups, uploads) should be stored.
    
    Priority:
    1. JANKALYAN_DATA_DIR environment variable (if explicitly configured).
    2. When Frozen (packaged .exe): %APPDATA%/JankalyanBloodBank/data (on Windows) or ~/.jankalyan_bloodbank/data
    3. When in Development: <project_root>/database (or %APPDATA%/JankalyanBloodBank if desired)
    """
    custom_dir = os.environ.get('JANKALYAN_DATA_DIR')
    if custom_dir:
        data_dir = os.path.abspath(custom_dir)
    elif is_frozen():
        if sys.platform == 'win32':
            app_data = os.environ.get('APPDATA') or os.path.expanduser('~')
            data_dir = os.path.join(app_data, 'JankalyanBloodBank', 'data')
        elif sys.platform == 'darwin':
            data_dir = os.path.expanduser('~/Library/Application Support/JankalyanBloodBank/data')
        else:
            data_dir = os.path.expanduser('~/.jankalyan_bloodbank/data')
    else:
        # Development mode defaults to project database folder
        data_dir = os.path.join(get_base_dir(), 'database')

    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def get_db_path():
    """
    Returns the absolute path to the active SQLite database file (bloodbank.db).
    Supports JANKALYAN_DB_PATH override.
    """
    custom_db = os.environ.get('JANKALYAN_DB_PATH')
    if custom_db:
        db_path = os.path.abspath(custom_db)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        return db_path
    return os.path.normpath(os.path.join(get_data_dir(), 'bloodbank.db'))

def get_backup_dir():
    """
    Returns the directory where database backups can be saved.
    """
    backup_dir = os.path.join(os.path.dirname(get_data_dir()), 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir
