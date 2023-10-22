from pydantic import HttpUrl

from config import settings

prefix = "police-station"

HOST: HttpUrl = settings.APP_HOST
LOGIN_URL: HttpUrl = HttpUrl(f"{HOST}auth/{prefix}/login")
REGISTER_URL: HttpUrl = HttpUrl(f"{HOST}auth/{prefix}/register")
REFRESH_TOKEN_URL: HttpUrl = HttpUrl(f"{HOST}auth/refresh")
SEND_OTP_URL: HttpUrl = HttpUrl(f"{HOST}auth/{prefix}/send-otp")
VERIFY_EMAIL_URL: HttpUrl = HttpUrl(f"{HOST}auth/{prefix}/verify-email")
POLICE_STATION_DASHBOARD_URL: HttpUrl = HttpUrl(f"{HOST}{prefix}/dashboard")
