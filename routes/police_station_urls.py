from pydantic import HttpUrl

from config import settings

prefix = "police-station"

APP_HOST: HttpUrl = settings.APP_HOST
API_HOST: HttpUrl = settings.API_HOST
LOGIN_URL: HttpUrl = HttpUrl(f"{API_HOST}auth/{prefix}/login")
REGISTER_URL: HttpUrl = HttpUrl(f"{API_HOST}auth/{prefix}/register")
REFRESH_TOKEN_URL: HttpUrl = HttpUrl(f"{API_HOST}auth/refresh")
SEND_OTP_URL: HttpUrl = HttpUrl(f"{API_HOST}auth/{prefix}/send-otp")
VERIFY_EMAIL_URL: HttpUrl = HttpUrl(f"{API_HOST}auth/{prefix}/verify-email")
POLICE_STATION_DASHBOARD_URL: HttpUrl = HttpUrl(f"{APP_HOST}{prefix}/dashboard")
RESET_PASSWORD_URL: HttpUrl = HttpUrl(f"{APP_HOST}{prefix}/reset-password")
