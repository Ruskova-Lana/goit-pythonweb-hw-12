from unittest.mock import AsyncMock, patch

import pytest

from goit_hw_12.email_service import (
    send_password_reset_email,
    send_verification_email,
)


@pytest.mark.asyncio
async def test_send_verification_email():
    with patch("goit_hw_12.email_service.FastMail") as mock_fastmail:
        mock_instance = mock_fastmail.return_value
        mock_instance.send_message = AsyncMock()

        await send_verification_email("test@test.com", "test-token")

        mock_instance.send_message.assert_called_once()


@pytest.mark.asyncio
async def test_send_password_reset_email():
    with patch("goit_hw_12.email_service.FastMail") as mock_fastmail:
        mock_instance = mock_fastmail.return_value
        mock_instance.send_message = AsyncMock()

        await send_password_reset_email("test@test.com", "reset-token")

        mock_instance.send_message.assert_called_once()