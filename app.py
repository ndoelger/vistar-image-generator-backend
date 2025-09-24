from flask import Flask
from flask_cors import CORS


from routes import generate, upload
from utils.logging_config import setup_logging

from pypdf import PdfReader


logger = setup_logging()

app = Flask(__name__)
CORS(app)


@app.route("/upload", methods=["POST"])
def upload_route():
    return upload.upload_local()


@app.route("/generate", methods=["POST"])
def generate_route():
    return generate.openai_gen()
