# backend/auth.py

from flask import Blueprint, request, jsonify
import sqlite3
import hashlib
import os

auth_bp = Blueprint("auth", __name__)

DB_PATH = "backend/db/users.db"

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                    (username, hash_password(password)))
        conn.commit()
        return jsonify({"message": "Signup successful"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409
    finally:
        conn.close()

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cur.fetchone()
    conn.close()

    if result and result[0] == hash_password(password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
