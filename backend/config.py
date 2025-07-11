
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your-very-secure-dev-key"
    UPLOAD_FOLDER = "backend/docs"
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20MB file upload limit
