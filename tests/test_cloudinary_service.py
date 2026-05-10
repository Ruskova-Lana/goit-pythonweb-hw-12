from unittest.mock import MagicMock, patch

from goit_hw_12.cloudinary_service import upload_avatar


def test_upload_avatar():
    file = MagicMock()
    file.file = MagicMock()

    with patch("goit_hw_12.cloudinary_service.cloudinary.uploader.upload") as mock_upload:
        mock_upload.return_value = {
            "secure_url": "https://res.cloudinary.com/test/avatar.jpg"
        }

        result = upload_avatar(file, user_id=1)

        assert result == "https://res.cloudinary.com/test/avatar.jpg"
        mock_upload.assert_called_once()