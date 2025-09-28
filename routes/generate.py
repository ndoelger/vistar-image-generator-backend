from flask import request, send_from_directory
from utils import file_utils, pdf_service
from services import openai_service

import base64
import os, glob

import boto3


from PIL import Image

import logging

logger = logging.getLogger(__name__)


def openai_gen():
    try:

        logger.info("Unpackaging images from zip")
        assets_zip = request.files.get("assets")

        images = [
            f
            for f in file_utils.unzip(assets_zip)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
            and "__MACOSX" not in f
            and not os.path.basename(f).startswith("._")
        ]

        print(images)

        copy = request.form.get("copy")
        primary_col = request.form.get("priCol")
        secondary_col = request.form.get("secCol")
        tertiary_col = request.form.get("terCol")

        logger.info("Converting brand book to prompt")
        logger.info("Getting text")
        copy_text = f"""
                    Generate a digital advertisement based on the attached reference photo.
                    Include the attached logo and attached product images. For branding, use:
                    Primary Color: {primary_col}
                    Secondary Color: {secondary_col}
                    Tertiary Color: {tertiary_col}
                    Have the copy say "{copy}".
                    Thank you!
                    """

        logger.info(f"Generating Image w/ prompt")

        gen_img = openai_service.gen_img(copy_text, images)

        logger.info(f"Saving Image Locally")
        upload_path = os.path.join(os.getcwd(), "img.png")

        with open(upload_path, "wb") as f:
            f.write(gen_img)

        logger.info(f"Saving Image to s3")

        boto3.setup_default_session(profile_name="default")
        s3: boto3.client = boto3.client("s3")

        with open(upload_path, "rb") as f:
            s3.upload_fileobj(f, "vistar-dc", f"2025/09/ai-innovation/img1080.png")

        print("Success!")
        return "https://vistar-dc.s3.us-east-1.amazonaws.com/2025/09/ai-innovation/img1080.png"

    except Exception as e:
        print(f"ERROR: {e}")
        return "fail!"
