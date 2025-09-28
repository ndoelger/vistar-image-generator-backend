from flask import request, redirect

import logging

logger = logging.getLogger(__name__)


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