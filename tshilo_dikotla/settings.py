"""
Django settings for tshilo_dikotla project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import sys
import os
import socket


# EDC specific settings
APP_NAME = 'td'
LIVE_SERVER = 'td.bhp.org.bw'
TEST_HOSTS = ['edc4.bhp.org.bw', 'tdtest.bhp.org.bw', 'tdtest2.bhp.org.bw']
DEVELOPER_HOSTS = [
    'mac2-2.local', 'ckgathi', 'one-2.local', 'One-2.local', 'tsetsiba', 'leslie', 'keletso-mac']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if socket.gethostname() == LIVE_SERVER:
    KEY_PATH = '/home/django/source/tshilo_dikotla/keys'
elif socket.gethostname() in TEST_HOSTS + DEVELOPER_HOSTS:
    KEY_PATH = os.path.join(BASE_DIR, 'crypto_fields')
elif 'test' in sys.argv:
    KEY_PATH = os.path.join(BASE_DIR, 'crypto_fields')
else:
    raise TypeError(
        'Warning! Unknown hostname for KEY_PATH. \n'
        'Getting this wrong on a LIVE SERVER will corrupt your encrypted data!!! \n'
        'Expected hostname to appear in one of '
        'settings.LIVE_SERVER, settings.TEST_HOSTS or settings.DEVELOPER_HOSTS. '
        'Got hostname=\'{}\'\n'.format(socket.gethostname()))

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'simple_history',
    'rest_framework',
    'rest_framework.authtoken',
    'django_js_reverse',
    'corsheaders',
    'crispy_forms',
    'django_crypto_fields.apps.AppConfig',
    'django_revision.apps.AppConfig',
    'edc_call_manager.apps.AppConfig',
    'edc_code_lists.apps.AppConfig',
    'edc_death_report.apps.AppConfig',
    'edc_export.apps.AppConfig',
    'edc_locator.apps.AppConfig',
    'edc_offstudy.apps.AppConfig',
    'edc_registration.apps.AppConfig',
    'edc_rule_groups.apps.AppConfig',
    'edc_visit_schedule.apps.AppConfig',
    'edc_sync.apps.AppConfig',
    'td.apps.AppConfig',
    'td_dashboard.apps.AppConfig',
    'td_infant.apps.AppConfig',
    'td_lab.apps.AppConfig',
    'td_list.apps.AppConfig',
    'td_maternal.apps.AppConfig',
    'tshilo_dikotla.apps.EdcAppointmentAppConfig',
    'tshilo_dikotla.apps.EdcBaseAppConfig',
    'tshilo_dikotla.apps.EdcConsentAppConfig',
    'tshilo_dikotla.apps.EdcDeviceAppConfig',
    'tshilo_dikotla.apps.EdcIdentifierAppConfig',
    # 'tshilo_dikotla.apps.EdcLabAppConfig',
    'tshilo_dikotla.apps.EdcLabelAppConfig',
    'tshilo_dikotla.apps.EdcMetadataAppConfig',
    'tshilo_dikotla.apps.EdcProtocolAppConfig',
    'tshilo_dikotla.apps.EdcTimepointAppConfig',
    'tshilo_dikotla.apps.EdcVisitTrackingAppConfig',
    'tshilo_dikotla.apps.AppConfig',
]


SECRET_KEY = 'sdfsd32fs#*@(@dfsdf'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'tshilo_dikotla.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'tshilo_dikotla.wsgi.application'


if 'test' in sys.argv:
    DEBUG = False
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )
    cnf = 'test_default.cnf'
else:
    cnf = 'default.cnf'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, 'etc', cnf),
        },
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if 'test' in sys.argv and 'mysql' not in DATABASES.get('default').get('ENGINE'):
    MIGRATION_MODULES = {
        "django_crypto_fields": None,
        "edc_call_manager": None,
        "edc_appointment": None,
        "edc_call_manager": None,
        "edc_code_lists": None,
        "edc_consent": None,
        "edc_death_report": None,
        "edc_export": None,
        "edc_identifier": None,
        "edc_metadata": None,
        "edc_rule_groups": None,
        "edc_registration": None,
        "edc_sync": None,
        "td": None,
        "td_infant": None,
        "td_lab": None,
        "td_list": None,
        "td_maternal": None,
        'django_crypto_fields': None}

FIELD_MAX_LENGTH = 'default'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = True
TIME_ZONE = 'UTC'

LANGUAGES = (
    ('tn', 'Setswana'),
    ('en', 'English'))


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

DEFAULT_STUDY_SITE = '40'
ALLOW_MODEL_SERIALIZATION = True

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

CRISPY_TEMPLATE_PACK = 'bootstrap3'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# try:
#     config = configparser.ConfigParser()
#     config.read(os.path.join(ETC_DIR, 'edc_sync.ini'))
#     CORS_ORIGIN_WHITELIST = tuple(config['corsheaders'].get('cors_origin_whitelist').split(','))
#     CORS_ORIGIN_ALLOW_ALL = config['corsheaders'].getboolean('cors_origin_allow_all', True)
# except KeyError:
#     CORS_ORIGIN_WHITELIST = None
#     CORS_ORIGIN_ALLOW_ALL = True
# REST_FRAMEWORK = {
#     'PAGE_SIZE': 1,
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.TokenAuthentication',
#     ),
# }
