# backend/utils/session_memory.py

import time

# Store history per user: {user_id: [(message, timestamp), ...]}
user_sessions = {}

# Settings
MAX_MESSAGES = 5            # Max past messages to remember
EXPIRY_SECONDS = 900        # 15 minutes

def add_user_message(user_id, message):
    now = time.time()
    if user_id not in user_sessions:
        user_sessions[user_id] = []
    user_sessions[user_id].append((message, now))

    # Trim old messages or excess
    user_sessions[user_id] = [
        (msg, ts) for msg, ts in user_sessions[user_id]
        if now - ts <= EXPIRY_SECONDS
    ][-MAX_MESSAGES:]

def get_user_context(user_id):
    now = time.time()
    if user_id not in user_sessions:
        return ""
    return " ".join([msg for msg, ts in user_sessions[user_id] if now - ts <= EXPIRY_SECONDS])
