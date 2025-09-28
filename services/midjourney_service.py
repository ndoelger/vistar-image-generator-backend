from midjourney_sdk_py import Midjourney
from dotenv import load_dotenv
import os, logging

logger = logging.getLogger(__name__)


load_dotenv()


def midj_gen():
    try:
        discord_channel_id = os.getenv("DISCORD_CHANNEL_ID")
        discord_user_token = os.getenv("DISCORD_USER_TOKEN")
        discord_session_id = os.getenv("DISCORD_SESSION_ID")

        print(discord_channel_id, discord_session_id, discord_user_token)
        midjourney = Midjourney(
            discord_channel_id, discord_user_token, discord_session_id
        )

        print(midjourney)

        prompt = "A big smile"
        # options = {"ar": "3:2", "v": "6.1"}

        logger.info("Generating image")

        pic = midjourney.generate(prompt=prompt)
        print(f"pic: {pic}")
        return pic["upscaled_photo_url"]
    except Exception as e:
        logger.error(e)
