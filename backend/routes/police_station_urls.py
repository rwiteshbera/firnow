from pydantic import HttpUrl

from config import Mode, settings

prefix = "police-station"

API_HOST: HttpUrl = settings.API_HOST

if settings.MODE == Mode.DEV:
    APP_HOST: HttpUrl = settings.APP_HOST
    LOGIN_URL: HttpUrl = HttpUrl(f"{API_HOST}{prefix}/login")
    REGISTER_URL: HttpUrl = HttpUrl(f"{API_HOST}{prefix}/register")
    REFRESH_TOKEN_URL: HttpUrl = HttpUrl(f"{API_HOST}refresh")
    SEND_OTP_URL: HttpUrl = HttpUrl(f"{API_HOST}{prefix}/send-otp")
    VERIFY_EMAIL_URL: HttpUrl = HttpUrl(f"{API_HOST}{prefix}/verify-email")
    POLICE_STATION_DASHBOARD_URL: HttpUrl = HttpUrl(f"{APP_HOST}{prefix}/dashboard")
    RESET_PASSWORD_URL: HttpUrl = HttpUrl(f"{APP_HOST}{prefix}/reset-password")

else:
    APP_HOST: HttpUrl = settings.APP_HOST
    LOGIN_URL: HttpUrl = HttpUrl(f"{API_HOST}auth/{prefix}/login")
    REGISTER_URL: HttpUrl = HttpUrl(f"{API_HOST}auth/{prefix}/register")
    REFRESH_TOKEN_URL: HttpUrl = HttpUrl(f"{API_HOST}auth/refresh")
    SEND_OTP_URL: HttpUrl = HttpUrl(f"{API_HOST}auth/{prefix}/send-otp")
    VERIFY_EMAIL_URL: HttpUrl = HttpUrl(f"{API_HOST}auth/{prefix}/verify-email")
    POLICE_STATION_DASHBOARD_URL: HttpUrl = HttpUrl(f"{APP_HOST}{prefix}/dashboard")
    RESET_PASSWORD_URL: HttpUrl = HttpUrl(f"{APP_HOST}{prefix}/reset-password")
