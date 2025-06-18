

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6xrx_zl*u-^b8z%do(bt729g%*yk4vh1msep(nn6j9dqwqm$ti'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hospital',
    'django_otp',
    'django_otp.plugins.otp_totp',  # Time-based OTP
    'django_otp.plugins.otp_static',  # Backup codes
    'two_factor',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hospital_mgnt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [BASE_DIR / "templates"],
          'DIRS': [
            os.path.join(BASE_DIR, 'hospital/templates'),
            os.path.join(BASE_DIR, 'templates'),
         ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hospital_mgnt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'my_HMS_db',
        'HOST': '.\\SQLEXPRESS',  # Try with IP address
        'PORT': '1433',
        # 'HOST': 'localhost\\SQLEXPRESS',  # Changed to localhost
        # 'PORT': '',  # Empty for named instances
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'trusted_connection': 'yes',
            'extra_params': "TrustServerCertificate=yes",
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'hospital/static'),
]

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # For Gmail, or your SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'varmashivamtyu@gmail.com'  # Your email
EMAIL_HOST_PASSWORD = 'virx kzdi jubr fchs'  # Your email password or app password
DEFAULT_FROM_EMAIL = 'varmashivamtyu@gmail.com'  # Your email
SITE_NAME = "LifeLine Hospital"  # Will be used in emails
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'hospital', 'static')]

import os
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# In settings.py (development only)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Add these authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'two_factor.auth_backends.TwoFactorBackend',
]

# Required for two-factor auth
# LOGIN_URL = 'two_factor:login'
# LOGIN_REDIRECT_URL = 'two_factor:profile'

# AUTH_USER_MODEL = 'accounts.CustomUser'

# LOGIN_URL = 'two_factor:login'
# LOGIN_REDIRECT_URL = 'admin_dashboard'  # Change to your desired redirect

LOGIN_URL = 'two_factor:login'
LOGIN_REDIRECT_URL = 'admin_dashboard' 
TWO_FACTOR_PATCH_ADMIN = False  # We're handling admin separately
TWO_FACTOR_REMEMBER_COOKIE_AGE = 86400 * 30  # 30 days

# Disable phone verification if not needed
TWO_FACTOR_CALL_GATEWAY = None
TWO_FACTOR_SMS_GATEWAY = None