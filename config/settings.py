"""
Django settings for config project.
"""

import logging
from datetime import timedelta
from pathlib import Path

# Loyihaning asosiy papkasi (BASE_DIR) joylashuvi
BASE_DIR = Path(__file__).resolve().parent.parent

# Maxfiy kalit (Secret key)
SECRET_KEY = 'django-insecure-1t0cd6bd@ivcfubb@=55njss(2spsz@uo)5ih(lt!lqf5g^*oe'

# Debug rejimini yoqish (Dev muhit uchun)
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition
# Loyihaga ulangan barcha dasturlar va uchinchi tomon kutubxonalari
INSTALLED_APPS = [
    "django.contrib.admin",          # Django admin paneli
    "django.contrib.auth",           # Autentifikatsiya tizimi
    "django.contrib.contenttypes",   # Kontent turlari tizimi
    "django.contrib.sessions",       # Sessiyalarni boshqarish
    "django.contrib.messages",       # Xabarlarni ko'rsatish
    "django.contrib.staticfiles",    # Statik fayllar (CSS, JS) bilan ishlash
    
    # Uchinchi tomon kutubxonalari (Third-party)
    "rest_framework",                # Django REST Framework
    "rest_framework_simplejwt",      # JWT Token autentifikatsiyasi[cite: 1]
    "django_filters",                # Ma'lumotlarni filterlash vositasi
    "drf_spectacular",               # Swagger API hujjatlashtirish vositasi[cite: 1]
    "corsheaders",                   # CORS so'rovlarini boshqarish[cite: 1]
    
    # Mahalliy loyiha ilovasi
    "core",                          # Asosiy biznes mantiq ilovasi[cite: 1]
]

# So'rov va javoblar orasida ishlaydigan vositachi dasturlar (Middleware)
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",                    # CORS ni eng birinchi tekshirish[cite: 1]
    "django.middleware.security.SecurityMiddleware",            # Xavfsizlik sozlamalari
    "django.contrib.sessions.middleware.SessionMiddleware",      # Sessiyalar xizmati
    "django.middleware.common.CommonMiddleware",                # Umumiy middleware
    "django.middleware.csrf.CsrfViewMiddleware",                # CSRF hujumlaridan himoya
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Foydalanuvchini aniqlash
    "django.contrib.messages.middleware.MessageMiddleware",      # Xabarlarni yetkazish
    "django.middleware.clickjacking.XFrameOptionsMiddleware",   # Clickjacking dan himoya
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Ma'lumotlar bazasi sozlamasi (SQLite3)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # Bazaning drayveri
        "NAME": BASE_DIR / "db.sqlite3",          # Baza fayli joylashuvi
    }
}


# Parol mustahkamligini tekshirish
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Standart User o'rniga maxsus core.User modelini belgilash[cite: 1]
AUTH_USER_MODEL = "core.User"


# Django REST Framework global sozlamalari
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # JWT asosisiy autentifikatsiya[cite: 1]
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",     # Swagger sxemasi generatori[cite: 1]
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",  # Sahifalash turi[cite: 1]
    "PAGE_SIZE": 10,  # Har bir sahifada 10 tadan ma'lumot qaytariladi[cite: 1]
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",  # Filterlash backend'i
    ),
}


# JWT Token sozlamalari (Aprel / Yaroqlilik muddatlari)
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),     # Access token 1 kun amal qiladi
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),    # Refresh token 7 kun amal qiladi
    "ROTATE_REFRESH_TOKENS": True,
    "AUTH_HEADER_TYPES": ("Bearer",),               # Authorization: Bearer <token>
}


# Swagger UI (drf-spectacular) sozlamalari[cite: 1]
SPECTACULAR_SETTINGS = {
    "TITLE": "Ovqat Buyurtma API",                         # API sarlavhasi[cite: 1]
    "DESCRIPTION": "Ovqat buyurtma qilish backend REST API hujjatlari",  # Tavsifi[cite: 1]
    "VERSION": "1.0.0",                                     # Versiyasi[cite: 1]
}


# Barcha manbalardan kelgan so'rovlarga ruxsat berish (CORS)[cite: 1]
CORS_ALLOW_ALL_ORIGINS = True


# Tizim hodisalarini logga yozish (Logging) sozlamalari[cite: 1]
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",  # Log yozish formati[cite: 1]
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "app.log",                         # Log saqlanadigan fayl nomi[cite: 1]
            "formatter": "verbose",
        },
    },
    "loggers": {
        "core": {
            "handlers": ["console", "file"],                # Konsol va faylga yuborish[cite: 1]
            "level": "INFO",
            "propagate": True,
        },
    },
}


# Internatsionalizatsiya va Vaqt
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tashkent"  # Toshkent vaqt zonasi
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"