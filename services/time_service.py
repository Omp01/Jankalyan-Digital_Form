"""
Indian Standard Time (IST - Asia/Kolkata, UTC+05:30) Service
============================================================
Provides standardized time calculation, timestamp creation, and formatting
for all blood bank operations, audit logging, signatures, and reports.
"""

from datetime import datetime, timezone, timedelta

try:
    from zoneinfo import ZoneInfo
    IST_TZ = ZoneInfo("Asia/Kolkata")
except Exception:
    IST_TZ = timezone(timedelta(hours=5, minutes=30), name="IST")

def get_ist_tz():
    """Returns the Indian Standard Time timezone object."""
    return IST_TZ

def get_ist_now():
    """Returns current aware datetime in Indian Standard Time (IST)."""
    return datetime.now(IST_TZ)

def get_ist_timestamp_str():
    """Returns current timestamp string in IST: 'YYYY-MM-DD HH:MM:SS'."""
    return get_ist_now().strftime("%Y-%m-%d %H:%M:%S")

def get_ist_date_str():
    """Returns current date string in IST: 'YYYY-MM-DD'."""
    return get_ist_now().strftime("%Y-%m-%d")

def format_ist_display(val, include_time=True):
    """
    Converts a date or timestamp string to Indian display format:
    'DD-MM-YYYY HH:MM:SS' or 'DD-MM-YYYY'.
    """
    if not val:
        return ''
    s = str(val).strip()
    if not s or s in ('N/A', 'None', 'null'):
        return s

    # Handle ISO strings with 'T' or space
    parts = s.replace('T', ' ').split(' ')
    date_part = parts[0]
    time_part = ' '.join(parts[1:]) if len(parts) > 1 else ''

    dp = date_part.split('-')
    if len(dp) == 3:
        if len(dp[0]) == 4:  # YYYY-MM-DD -> DD-MM-YYYY
            formatted_date = f"{dp[2]}-{dp[1]}-{dp[0]}"
        elif len(dp[0]) == 2 and len(dp[2]) == 4:  # DD-MM-YYYY
            formatted_date = date_part
        else:
            formatted_date = date_part
    else:
        formatted_date = date_part

    if time_part and include_time:
        # Strip fractional seconds or timezone offsets for clean display
        time_clean = time_part.split('.')[0].split('+')[0]
        return f"{formatted_date} {time_clean}".strip()
    return formatted_date
