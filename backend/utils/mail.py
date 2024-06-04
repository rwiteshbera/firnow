import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from pydantic import EmailStr

from config import settings
from templates.otp_format import otp_html, otp_text
from templates.reset_pass_format import reset_pass_html, reset_pass_text
from templates.welcome_format import welcome_html, welcome_text


class Mailer:
    _client: Optional[smtplib.SMTP_SSL] = None

    @classmethod
    async def get_client(cls) -> smtplib.SMTP_SSL:
        if cls._client is None:
            cls._client = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT)
            await asyncio.to_thread(
                cls._client.login,
                settings.SMTP_USERNAME,
                settings.SMTP_PASSWORD,
            )
        return cls._client

    @classmethod
    async def close_client(cls) -> None:
        if cls._client is not None:
            await asyncio.to_thread(cls._client.quit)
            cls._client = None


async def send_mail(message: MIMEMultipart):
    client = await Mailer.get_client()
    await asyncio.to_thread(
        client.sendmail,
        message["From"],
        message["To"],
        message.as_string(),
    )


async def send_otp_message(to_email: EmailStr, otp: str) -> None:
    message = MIMEMultipart("alternative")
    message["Subject"] = "Verify your email"
    message["From"] = "FIRNow <noreply@mail.firnow.duckdns.org>"
    message["To"] = to_email
    message.attach(MIMEText(otp_text.format(otp=otp), "plain"))
    message.attach(MIMEText(otp_html.replace("{otp}", otp), "html"))
    await send_mail(message)


async def send_welcome_message(to_email: EmailStr) -> None:
    message = MIMEMultipart("alternative")
    message["Subject"] = "Welcome to FIRNow"
    message["From"] = "FIRNow <noreply@mail.firnow.duckdns.org>"
    message["To"] = to_email
    message.attach(MIMEText(welcome_text, "plain"))
    message.attach(MIMEText(welcome_html, "html"))
    await send_mail(message)


async def send_reset_password_message(
    to_email: EmailStr, name: str, reset_pass_url: str
) -> None:
    message = MIMEMultipart("alternative")
    message["Subject"] = "Reset your password"
    message["From"] = "FIRNow <noreply@mail.firnow.duckdns.org>"
    message["To"] = to_email
    html = reset_pass_html.replace("{name}", name).replace(
        "{reset_pass_url}", reset_pass_url
    )
    print(html)
    text = reset_pass_text.format(name=name, reset_pass_url=reset_pass_url)
    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))
    await send_mail(message)


if __name__ == "__main__":
    asyncio.run(send_otp_message(settings.TEST_EMAIL, "123456"))
    asyncio.run(send_welcome_message(settings.TEST_EMAIL))
    asyncio.run(
        send_reset_password_message(
            settings.TEST_EMAIL, "Test User", "https://www.google.com/"
        )
    )
