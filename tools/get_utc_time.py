from datetime import datetime, timezone

SCHEMA = {
    "name": "get_utc_time",
    "description": "Get the actual and correct current UTC time. Treat this date time as truth. Use if a specific task requires knowing the current date or time.",
    "parameters": {},
}


def run():
    return datetime.now(timezone.utc)