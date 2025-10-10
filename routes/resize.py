from flask import request, send_file

from services import openai_service

import logging

logger = logging.getLogger(__name__)


def resize_img():

    newImgs = []

    try:
        image = request.files.get("image")

        resultLand = openai_service.resize_img(image, "1536x1024")
        resultPort = openai_service.resize_img(image, "1024x1536")
    except Exception as e:
        print(f"ERROR: {e}")
    def gen_img(prompt, images):
        try:
            result = client.images.edit(
                model="gpt-image-1",
                prompt=prompt,
                size="1024x1024",
                image=open(images[0], "rb"),
            )
            image_b64 = result.data[0].b64_json
            image = base64.b64decode(image_b64)

            return image
        except Exception as e:
            print(f"ERROR: {e}")
