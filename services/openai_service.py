from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()

API_KEY = os.getenv("API_KEY")

client = OpenAI(api_key=API_KEY)


def summarize_brand(brand_text):
    try:
        brand_book_res = client.responses.create(
            model="chatgpt-4o-latest",
            input=[
                {
                    "role": "user",
                    "role": "user",
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

        return brand_book_res.output[0].content[0].text
    except Exception as e:
         print(f"ERROR: {e}")

def gen_img(prompt, images):
    try:
        result = client.images.edit(
            model="gpt-image-1",
            prompt=prompt,
            image=[open(img, "rb") for img in images],
        )
        image_b64 = result.data[0].b64_json
        image = base64.b64decode(image_b64)
        return image

    except Exception as e:
            print(f"ERROR: {e}")

def resize_img(sizes, images):
    try:
        result = client.images.edit(
            model="gpt-image-1",
            prompt=f"Resize the attached image to these sizes: {sizes}",
            image=open(images[0], "rb"),
        )
        image_b64 = result.data[0].b64_json
        image = base64.b64decode(image_b64)
    
        return image
    except Exception as e:
            print(f"ERROR: {e}")