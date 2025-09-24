from flask import request
from utils import file_utils, pdf_service
from services import openai_service

import os, glob

import logging

logger = logging.getLogger(__name__)


def openai_gen():
    try:
        # logger.info("Extracting information from Brand Book")
        # brand_book = request.files.get("brandBook")

        # text = pdf_service.extract_text_from_pdf(brand_book)

        # brand_book_response = openai_service.summarize_brand(text)

        # print(brand_book_response)

        logger.info("Unpackaging images from zip")
        assets_zip = request.files.get("assets")

        images = [
            f for f in file_utils.unzip(assets_zip)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
            and "__MACOSX" not in f
            and not os.path.basename(f).startswith("._")
        ]

        print(images)


        logger.info("Converting brand book to prompt")
        logger.info("Getting text")
        copy_text = """
                    Generate a digital advertisement combining the reference pictures. Have the copy say "perfect time for a cup of joe!"
                    """

        logger.info(f"Generating Image w/ prompt")

        gen_img = openai_service.gen_img(copy_text, images)

        logger.info(f"Saving Image")
        upload_path = os.path.join(os.getcwd(), "img.png")

        with open(upload_path, "wb") as f:
            f.write(gen_img)

        print("Success!")
        return "Success"

    except Exception as e:
        print(f"ERROR: {e}")
        return "fail!"
