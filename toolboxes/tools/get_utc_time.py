#Copyright (c) 2026 Gene B. Denney. All Rights Reserved.

from datetime import datetime, timezone

SCHEMA = {
    "name": "get_utc_time",
    "description": "Get the actual and correct current UTC time. Treat this date time as truth. Use if a specific task requires knowing the current date or time.",
    "parameters": {
        "type": "object",
        "properties": {}
    },
}


def run():
    return datetime.now(timezone.utc)