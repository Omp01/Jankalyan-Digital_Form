from functools import wraps
from flask import session, jsonify

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Authentication required. Please log in.'}), 401
        return f(*args, **kwargs)
    return decorated_function

def roles_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'success': False, 'message': 'Authentication required. Please log in.'}), 401
            user_role = session.get('role')
            if user_role not in allowed_roles:
                return jsonify({'success': False, 'message': f'Access denied. Role "{user_role}" is not permitted.'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
