from flask import Flask, request, redirect
from flask_cors import CORS
from dotenv import load_dotenv

from openai import OpenAI

import os, base64

from pypdf import PdfReader


import logging
import boto3
from botocore.exceptions import ClientError

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

load_dotenv()

API_KEY = os.getenv("API_KEY")

upload_dir = os.path.join(os.getcwd(), "uploads")
os.makedirs(upload_dir, exist_ok=True)


@app.route("/", methods=["POST"])
def upload_local():

    logger.info("Asset upload stage")
    logger.info("Setting up s3")
    boto3.setup_default_session(profile_name="default")
    s3 = boto3.client("s3")

    logger.info("Parsing form data")
    brand_book = request.files.get("brandBook")
    assets_zip = request.files.get("assets")
    copy = request.form.get("copy")

    logger.info("Uploading to s3")
    s3.upload_fileobj(
        brand_book, "vistar-dc", f"2025/09/ai-innovation/{brand_book.filename}"
    )

    s3.upload_fileobj(
        assets_zip, "vistar-dc", f"2025/09/ai-innovation/{assets_zip.filename}"
    )

    s3.put_object(
        Body=copy,
        Bucket="vistar-dc",
        Key=f"2025/09/ai-innovation/copy.txt",
    )

    logger.info("Redirecting to /generate")
    return redirect("/generate")
    # brand_file_name = secure_filename(brand_book.filename)
    # assets_zip_name = secure_filename(assets_zip.filename)

    # brand_book.save(os.path.join(upload_dir, brand_file_name))
    # assets_zip.save(os.path.join(upload_dir, assets_zip_name))

    # copy_path = os.path.join(upload_dir, "copy.txt")

    # with open(copy_path, "w") as t:
    #     t.write(copy)


@app.route("/generate", methods=["POST"])
def openai_gen():
    try:
        logger.info("Setting up s3")
        boto3.setup_default_session(profile_name="default")
        s3 = boto3.client("s3")

        logger.info(f"Connecting to Open Client")
        client = OpenAI(api_key=API_KEY)

        logger.info("Extracting information from Brand Book")
        brand_book = request.files.get("brandBook")

        reader = PdfReader(brand_book.stream)
        text = []

        for page in reader.pages:
            text.append(page.extract_text() or "")

        brand_text = "\n".join(text)

        brand_book_response = client.responses.create(
            model="chatgpt-4o-latest",
            input=[
                {
                    "role": "assistant",
                    "content": f"""Summarize the following brand book text into clear design guidelines.
                    Focus on:
                    - Color palette
                    - Typography
                    - Logo usage
                    - Image/illustration style
                    - Voice & tone

                    Brand Book:
                    {brand_text}
                    """,
                }
            ],
        )

        print(brand_book_response.output_text)

        return

        logger.info("Converting brand book to prompt")

        logger.info("Getting text")
        response = s3.get_object(
            Bucket="vistar-dc", Key="2025/09/ai-innovation/copy.txt"
        )

        copy_text = response["Body"].read().decode("utf-8")

        logger.info(f"Got text: {copy_text}")

        logger.info(f"Generating Image")
        result = client.images.generate(
            model="gpt-image-1", prompt=copy_text, size="1x1024", quality="low"
        )

        image_b64 = result.data[0].b64_json
        image = base64.b64decode(image_b64)

        logger.info(f"Savimng Image")
        upload_path = os.path.join(os.getcwd(), "img.png")

        with open(upload_path, "wb") as f:
            f.write(image)

        print("Success!")
        return image_b64

    except Exception as e:
        print(f"ERROR: {e}")
        return "fail!"

    # image_path = os.path.join(upload_dir, "copy.txt")

    # return "Success!"


# @app.route('/')
# def upload_aws():
#     try:
#         boto3.setup_default_session(profile_name="default")
#         s3 = boto3.client("s3")

#         s3.upload_file(
#                     Body=pdf,
#                     Bucket="vistar-dc",
#                     Key=f"2025/09/ai-innovation/test/test.pdf",
#                 )
#     except ClientError as e:
#         logging.error(e)
