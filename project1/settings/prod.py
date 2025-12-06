from .common import *
import os
import dj_database_url

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = False

# Allowed hosts
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)

# Database
DATABASES = {
    "default": dj_database_url.config(conn_max_age=600)
}
DATABASES["default"]["OPTIONS"] = {"sslmode": "require"}

# Redis / Celery
REDIS_URL = os.environ.get("REDIS_URL")
if not REDIS_URL:
    raise Exception("REDIS_URL environment variable is required!")

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# Caches
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() in ["true", "1", "yes"]
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# Static & media
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# Security headers for production
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
