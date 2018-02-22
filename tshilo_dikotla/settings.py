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
import configparser
import socket
from unipath import Path

from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured

from .databases import (
    PRODUCTION_POSTGRES, TEST_HOSTS_POSTGRES, TRAVIS_POSTGRES, PRODUCTION_SECRET_KEY)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# EDC specific settings
APP_NAME = 'td'
LIVE_SERVER = 'td.bhp.org.bw'
TEST_HOSTS = ['edc4.bhp.org.bw', 'tdtest.bhp.org.bw']
DEVELOPER_HOSTS = ['leslie']

PROJECT_TITLE = 'Tshilo Dikotla'
INSTITUTION = 'Botswana-Harvard AIDS Institute'
PROTOCOL_REVISION = 'v1.0'
PROTOCOL_NUMBER = '085'

SOURCE_ROOT = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(1)
BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
MEDIA_ROOT = BASE_DIR.child('media')
PROJECT_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
PROJECT_ROOT = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(1)
ETC_DIR = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(
    2).child('etc')

if socket.gethostname() == LIVE_SERVER:
    KEY_PATH = '/home/django/source/keys'
elif socket.gethostname() in TEST_HOSTS + DEVELOPER_HOSTS:
    KEY_PATH = os.path.join(SOURCE_ROOT, 'crypto_fields/test_keys')
elif 'test' in sys.argv:
    KEY_PATH = os.path.join(SOURCE_ROOT, 'crypto_fields/test_keys')
else:
    raise TypeError(
        'Warning! Unknown hostname for KEY_PATH. \n'
        'Getting this wrong on a LIVE SERVER will corrupt your encrypted data!!! \n'
        'Expected hostname to appear in one of '
        'settings.LIVE_SERVER, settings.TEST_HOSTS or settings.DEVELOPER_HOSTS. '
        'Got hostname=\'{}\'\n'.format(socket.gethostname()))

DEBUG = True

ALLOWED_HOSTS = []
USE_X_FORWARDED_HOST = True

INSTALLED_APPS = [
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
    'django_revision',
    'edc_templates',
    'edc_identifier',
    'edc_lab.lab_packing',
    'edc_lab.lab_clinic_api',
    'edc_lab.lab_clinic_reference',
    'lis.labeling',
    'edc_appointment',
    'edc_base',
    'edc_configuration',
    'corsheaders',
    'crispy_forms',
    #     'edc_consent',
    'edc_constants',
    'edc_content_type_map',
    'edc_dashboard',
    'edc_data_manager',
    'edc_death_report',
    'edc_device',
    'edc_locator',
    'edc_meta_data',
    'edc_offstudy',
    'edc_registration',
    'edc_rule_groups',
    #     'edc_sync',
    'edc_sync_files',
    'django_appconfig_ini',
    'edc_code_lists',
    'edc_visit_schedule',
    'edc_visit_tracking',
    'call_manager',
    'edc_call_manager.apps.EdcCallManagerAppConfig',
    'tshilo_dikotla.apps.DjangoCryptoFieldsAppConfig',
    'tshilo_dikotla.apps.ConsentAppConfig',
    'tshilo_dikotla.apps.EdcSyncAppConfig',
    'tshilo_dikotla.apps.TshiloDikotlaConfig',
    'td_dashboard.apps.TdDashboardConfig',
    'td_infant.apps.TdInfantConfig',
    'td_lab.apps.TdLabConfig',
    'td_list.apps.TdListConfig',
    'registration.apps.RegistrationConfig',
    'td_maternal.apps.TdMaternalConfig',
]

if 'test' in sys.argv:
    #     INSTALLED_APPS.append('edc_testing')
    # TODO: Make this list auto generate from INSTALLED_APPS
    # Ignore running migrations on unit tests, greately speeds up tests.
    MIGRATION_MODULES = {"edc_registration": None,
                         "edc_content_type_map": None,
                         "edc_visit_schedule": None,
                         "edc_visit_tracking": None,
                         "edc_appointment": None,
                         "call_manager": None,
                         "edc_death_report": None,
                         "edc_identifier": None,
                         "edc_meta_data": None,
                         "edc_consent": None,
                         "edc_rule_groups": None,
                         "edc_data_manager": None,
                         "lab_packing": None,
                         "lab_clinic_api": None,
                         'django_crypto_fields': None,
                         "lab_clinic_reference": None,
                         "edc_death_report": None,
                         "edc_sync": None,
                         "edc_code_lists": None,
                         "edc_configuration": None,
                         "td_lab": None,
                         "td_infant": None,
                         "td_maternal": None,
                         "td_list": None,
                         "call_manager": None}


# MIDDLEWARE_CLASSES = (
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.locale.LocaleMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'simple_history.middleware.HistoryRequestMiddleware',)

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages")

ROOT_URLCONF = 'tshilo_dikotla.urls'

TEMPLATE_DIRS = ()

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader')

WSGI_APPLICATION = 'tshilo_dikotla.wsgi.application'

SECRET_KEY = 'sdfsd32fs#*@(@dfsdf'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

SOUTH_TESTS_MIGRATE = False

if socket.gethostname() in DEVELOPER_HOSTS:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    }
elif socket.gethostname() == 'ckgathi':
    SECRET_KEY = PRODUCTION_SECRET_KEY
    DATABASES = PRODUCTION_POSTGRES
elif socket.gethostname() in TEST_HOSTS:
    DATABASES = TEST_HOSTS_POSTGRES
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    }

# django auth
AUTH_PROFILE_MODULE = "bhp_userprofile.userprofile"

PROJECT_NUMBER = 'BHP085'
PROJECT_IDENTIFIER_PREFIX = '085'
PROJECT_IDENTIFIER_MODULUS = 7
IS_SECURE_DEVICE = True
FIELD_MAX_LENGTH = 'default'

# Internationalization
LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('tn', 'Setswana'),
    ('en', 'English'))

TIME_ZONE = 'Africa/Gaborone'

USE_I18N = True
USE_L10N = True
USE_TZ = False

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.child('static')

# admin
LOGIN_URL = '/{app_name}/login/'.format(app_name=APP_NAME)
LOGIN_REDIRECT_URL = '/{app_name}/'.format(app_name=APP_NAME)
LOGOUT_URL = '/{app_name}/logout/'.format(app_name=APP_NAME)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# edc.crytpo_fields encryption keys
# developers should set by catching their hostname instead of setting
# explicitly

GIT_DIR = BASE_DIR.ancestor(1)

STUDY_OPEN_DATETIME = timezone.datetime(2015, 10, 18, 0, 0, 0)

APP_LABEL = 'tshilo_dikotla'
LABEL_PRINTER_MAKE_AND_MODEL = ['Zebra ZPL Label Printer']

SUBJECT_APP_LIST = ['maternal', 'infant']
SUBJECT_TYPES = ['maternal', 'infant']
MAX_SUBJECTS = {'maternal': 499, 'infant': 499}
MINIMUM_AGE_OF_CONSENT = 18
MAXIMUM_AGE_OF_CONSENT = 64
AGE_IS_ADULT = 18
GENDER_OF_CONSENT = ['F']
DISPATCH_APP_LABELS = []

# if socket.gethostname() == LIVE_SERVER:
#     DEVICE_ID = 99
#     PROJECT_TITLE = '{} Live Server'.format(PROJECT_TITLE)
# elif socket.gethostname() in TEST_HOSTS:
#     DEVICE_ID = 99
#     PROJECT_TITLE = 'TEST (postgres): {}'.format(PROJECT_TITLE)
# elif socket.gethostname() in DEVELOPER_HOSTS:
#     DEVICE_ID = 99
#     PROJECT_TITLE = 'TEST (sqlite3): {}'.format(PROJECT_TITLE)
# elif 'test' in sys.argv:
#     DEVICE_ID = 99
#     PROJECT_TITLE = 'TEST (sqlite3): {}'.format(PROJECT_TITLE)
# else:
#     raise ImproperlyConfigured(
#         'Unknown hostname for full PROJECT_TITLE. Expected hostname to appear in one of '
#         'settings.LIVE_SERVER, settings.TEST_HOSTS or settings.DEVELOPER_HOSTS. '
#         'Got hostname=\'{}\''.format(socket.gethostname()))

DEVICE_ID = 99

SITE_CODE = '40'
SERVER_DEVICE_ID_LIST = [91, 92, 93, 94, 95, 96, 97, 99]
MIDDLEMAN_DEVICE_ID_LIST = [98]
if str(DEVICE_ID) == '98':
    PROJECT_TITLE = 'RESERVED FOR MIDDLE MAN'

CELLPHONE_REGEX = '^[7]{1}[12345678]{1}[0-9]{6}$'
TELEPHONE_REGEX = '^[2-8]{1}[0-9]{6}$'
DEFAULT_STUDY_SITE = '40'
ALLOW_MODEL_SERIALIZATION = True

PREVIOUS_CONSENT_VERSION = "1"
LASTEST_VERSION = "3"

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

try:
    config = configparser.ConfigParser()
    config.read(os.path.join(ETC_DIR, 'edc_sync.ini'))
    CORS_ORIGIN_WHITELIST = tuple(
        config['corsheaders'].get('cors_origin_whitelist').split(','))
    CORS_ORIGIN_ALLOW_ALL = config['corsheaders'].getboolean(
        'cors_origin_allow_all', True)
except KeyError:
    CORS_ORIGIN_WHITELIST = None
    CORS_ORIGIN_ALLOW_ALL = True
REST_FRAMEWORK = {
    'PAGE_SIZE': 1,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

# EDC_SYNC_ROLE = 'client'
