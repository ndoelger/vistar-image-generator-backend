from flask import Flask
from flask_cors import CORS


from routes import generate, upload, resize
from utils.logging_config import setup_logging


logger = setup_logging()

app = Flask(__name__)
CORS(app)


@app.route("/generate", methods=["POST"])
def generate_route():
    return generate.openai_gen()

@app.route("/resize", methods=["POST"])
def resize_route():
    return resize.resize_img()