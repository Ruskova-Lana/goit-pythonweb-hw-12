from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from goit_hw_10.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_verification_email(email: str, token: str):
    verification_link = f"http://127.0.0.1:8000/auth/confirmed_email/{token}"

    html = f"""
    <h2>Email verification</h2>
    <p>Please confirm your email by clicking the link below:</p>
    <a href="{verification_link}">Confirm email</a>
    """

    message = MessageSchema(
        subject="Confirm your email",
        recipients=[email],
        body=html,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)