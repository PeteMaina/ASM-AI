# backend/utils/file_reader.py

import os
import docx2txt
import PyPDF2

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_docx(file_path):
    return docx2txt.process(file_path)

def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def read_documents(folder="backend/docs"):
    all_text = ""
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if filename.endswith(".txt"):
            all_text += read_txt(path) + "\n"
        elif filename.endswith(".docx"):
            all_text += read_docx(path) + "\n"
        elif filename.endswith(".pdf"):
            all_text += read_pdf(path) + "\n"
    return all_text
