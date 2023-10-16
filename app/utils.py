import boto3
from fastapi import UploadFile, HTTPException, status
from PIL import Image
import secrets

from app.config import settings

aws_bucket_name = settings.BUCKET_NAME
s3 = boto3.resource(
    "s3",
    aws_access_key_id=settings.AWSAccessKeyId,
    aws_secret_access_key=settings.AWSSecretKey,
)


async def add_image(image: UploadFile):
    token_name = secrets.token_hex(12)
    file_name = f"{token_name}{image.filename}"
    supported_ext = ['png', 'jpg', 'jpeg']
    file_ext = file_name.split('.')[1]

    if file_ext not in supported_ext:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Unsupported file type.')
    bucket = s3.Bucket(aws_bucket_name)
    bucket.upload_fileobj(image.file, file_name)

    image_url = f"https://{aws_bucket_name}.s3.amazonaws.com/{file_name}"

    return image_url


async def delete_image(image_name: str):
    bucket = s3.Bucket(aws_bucket_name)

    return bucket.delete_fileobj(bucket, image_name)



