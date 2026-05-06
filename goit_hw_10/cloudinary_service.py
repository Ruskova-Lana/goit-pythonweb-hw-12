import cloudinary
import cloudinary.uploader

from goit_hw_10.config import settings


cloudinary.config(
    cloud_name=settings.CLOUDINARY_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


def upload_avatar(file, user_id: int):
    result = cloudinary.uploader.upload(
        file.file,
        public_id=f"user_{user_id}_avatar",
        folder="avatars",
        overwrite=True,
    )

    return result.get("secure_url")