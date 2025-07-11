# backend/routes.py

from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename

from backend.utils.file_reader import read_documents
from backend.ai_engine.chatbot import answer_question

routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/upload", methods=["POST"])
def upload_docs():
    if "files" not in request.files:
        return jsonify({"error": "No files uploaded"}), 400

    files = request.files.getlist("files")
    saved_files = []

    for file in files:
        filename = secure_filename(file.filename)
        file_path = os.path.join("backend/docs", filename)
        file.save(file_path)
        saved_files.append(filename)

    return jsonify({"message": "Files uploaded", "files": saved_files}), 200

@routes_bp.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        answer = answer_question(question)
        return jsonify({"answer": answer}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# routes.py

from flask import Blueprint, request, jsonify
from backend.ai_engine.chatbot import answer_question
from backend.auth import authenticate_user

api = Blueprint('api', __name__)

@api.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    token = data.get("token")
    question = data.get("question")

    if not token or not question:
        return jsonify({"error": "Missing token or question"}), 400

    user_id = authenticate_user(token)
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401

    response = answer_question(user_id, question)
    return jsonify({"response": response})
