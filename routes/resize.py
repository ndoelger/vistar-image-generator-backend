# from flask import request

# import logging

# logger = logging.getLogger(__name__)

# def resize_img():
#     image = request.files.get



#     def gen_img(prompt, images):
#     try:
#         result = client.images.edit(
#             model="gpt-image-1",
#             prompt=prompt,
#             size="1024x1024",
#             image=open(images[0], "rb"),
#         )
#         image_b64 = result.data[0].b64_json
#         image = base64.b64decode(image_b64)
    
#         return image
#     except Exception as e:
#             print(f"ERROR: {e}")