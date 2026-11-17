"""
Django settings for proj4 (Expense Tracker).

Same file works on your laptop AND on a hosting site.
Secret things (SECRET_KEY, DEBUG, database) are read from environment
variables when deployed, so nothing private goes to GitHub.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------
# Security / environment
# ---------------------------------------------------------------
# Locally the default values below are used. On the server you set
# SECRET_KEY and DEBUG=False as environment variables.
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-local-dev-key-change-me-on-server",
)

DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".pythonanywhere.com",
    ".onrender.com",
]
# Add your own domain(s) without touching code: EXTRA_HOSTS="example.com,www.example.com"
ALLOWED_HOSTS += [h.strip() for h in os.environ.get("EXTRA_HOSTS", "").split(",") if h.strip()]

CSRF_TRUSTED_ORIGINS = [
    "https://*.pythonanywhere.com",
    "https://*.onrender.com",
]


# ---------------------------------------------------------------
# Apps / middleware
# ---------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tracker",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # serves CSS/images on the server
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "proj4.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "proj4.wsgi.application"


# ---------------------------------------------------------------
# Database
# ---------------------------------------------------------------
# Laptop: SQLite file (db.sqlite3).
# Server (Render etc.): set DATABASE_URL and Postgres is used automatically.
if os.environ.get("DATABASE_URL"):
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.config(conn_max_age=600, ssl_require=not DEBUG)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------
# Static files
# ---------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"      # `collectstatic` puts files here

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}


# ---------------------------------------------------------------
# Login / logout behaviour
# ---------------------------------------------------------------
LOGIN_URL = "login"              # @login_required sends people here
LOGIN_REDIRECT_URL = "index"     # after login -> their own expense list
LOGOUT_REDIRECT_URL = "login"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Extra safety only when running on the server (DEBUG=False)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
