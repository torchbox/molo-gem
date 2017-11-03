# -*- coding: utf-8 -*-
"""
Django settings for base gem.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from os.path import abspath, dirname, join
from os import environ
import django.conf.locale
from django.conf import global_settings
from django.utils.translation import ugettext_lazy as _
import dj_database_url
import djcelery
from celery.schedules import crontab
djcelery.setup_loader()

# Absolute filesystem path to the Django project directory:
PROJECT_ROOT = dirname(dirname(dirname(abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "dqji)!xte^trgai!3c)_4)ftaoevwvbog-i&nl$#ef9xb+y*ab"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ENV = 'dev'

ALLOWED_HOSTS = ['*']


# Base URL to use when referring to full URLs within the Wagtail admin
# backend - e.g. in notification emails. Don't include '/admin' or
# a trailing slash
BASE_URL = 'http://example.com'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',


    'taggit',
    'modelcluster',

    'gem',
    'molo.core',
    'molo.profiles',
    'molo.surveys',
    'django_comments',
    'molo.commenting',
    'molo.yourwords',
    'molo.servicedirectory',
    'molo.polls',
    'molo.pwa',
    'fcm_django',
    'mote',

    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailsites',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsearch',
    'wagtail.wagtailredirects',
    'wagtail.wagtailforms',
    'wagtailmedia',
    'wagtail.contrib.settings',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.wagtailsitemaps',

    'wagtailsurveys',
    'wagtail_personalisation',
    'wagtailfontawesome',

    'mptt',
    'django.contrib.sites',
    'google_analytics',

    'raven.contrib.django.raven_compat',
    'djcelery',
    'django_cas_ng',
    'daterange_filter',
    'compressor',
    'notifications',
    'el_pagination',
    'import_export',
    'storages',
]

COMMENTS_APP = 'molo.commenting'
COMMENTS_FLAG_THRESHHOLD = 3
COMMENTS_HIDE_REMOVED = False

SITE_ID = 1

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'molo.core.middleware.ForceDefaultLanguageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',

    'molo.core.middleware.AdminLocaleMiddleware',
    'molo.core.middleware.NoScriptGASessionMiddleware',

    'gem.middleware.GemMoloGoogleAnalyticsMiddleware',
    'molo.core.middleware.MultiSiteRedirectToHomepage',
]

# Template configuration

# We have multiple layouts: use `base`, `malawi` or `springster`
# to switch between them.
SITE_LAYOUT_BASE = environ.get('SITE_LAYOUT_BASE', 'springster')
SITE_LAYOUT_2 = environ.get('SITE_LAYOUT_2', '')

DEFAULT_TEMPLATE = {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [join(PROJECT_ROOT, 'gem', 'templates', SITE_LAYOUT_2),
             join(PROJECT_ROOT, 'gem', 'templates', SITE_LAYOUT_BASE), ],
    'APP_DIRS': False,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'molo.core.context_processors.locale',
            'wagtail.contrib.settings.context_processors.settings',
            'gem.context_processors.default_forms',
            'gem.context_processors.detect_freebasics',
            'gem.processors.compress_settings',
        ],
        "loaders": [
            "django.template.loaders.filesystem.Loader",
            "mote.loaders.app_directories.Loader",
            "django.template.loaders.app_directories.Loader",
        ]
    },
}

TEMPLATES = [
    DEFAULT_TEMPLATE,
]

ROOT_URLCONF = 'gem.urls'
WSGI_APPLICATION = 'gem.wsgi.application'

# GEM-195
# Automatically log users out after 10 mins of inactivity
# Closing the browser window/tab will NOT end the session
SESSION_COOKIE_AGE = 60 * 10  # 10 minutes
SESSION_SAVE_EVERY_REQUEST = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# SQLite (simplest install)
DATABASES = {'default': dj_database_url.config(
    default='sqlite:///%s' % (join(PROJECT_ROOT, 'db.sqlite3'),))}

# PostgreSQL (Recommended, but requires the psycopg2 library and Postgresql
#             development headers)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'base',
#         'USER': 'postgres',
#         'PASSWORD': '',
#         'HOST': '',  # Set to empty string for localhost.
#         'PORT': '',  # Set to empty string for default.
#         # number of seconds database connections should persist for
#         'CONN_MAX_AGE': 600,
#     }
# }

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ALWAYS_EAGER = False
CELERY_IMPORTS = ('gem.tasks', 'molo.core.tasks', 'google_analytics.tasks')
BROKER_URL = environ.get('BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = environ.get(
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERYBEAT_SCHEDULE = {
    'rotate_content': {
        'task': 'molo.core.tasks.rotate_content',
        'schedule': crontab(minute=0),
    },
    'molo_consolidated_minute_task': {
        'task': 'molo.core.tasks.molo_consolidated_minute_task',
        'schedule': crontab(minute=0),
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = environ.get('LANGUAGE_CODE', 'en')
TIME_ZONE = 'Africa/Johannesburg'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = global_settings.LANGUAGES + [
    ('tl', 'Tagalog'),
    ('rw', 'Kinyarwanda'),
    ('ha', 'Hausa'),
    ('bn', 'Bengali'),
    ('my', 'Burmese'),
    ('ny', 'Chichewa'),
]

EXTRA_LANG_INFO = {
    'tl': {
        'bidi': False,
        'code': 'tl',
        'name': 'Tagalog',
        'name_local': 'Tagalog'
    },
    'rw': {
        'bidi': False,
        'code': 'rw',
        'name': 'Kinyarwanda',
        'name_local': 'Kinyarwanda'
    },
    'ha': {
        'bidi': False,
        'code': 'ha',
        'name': 'Hausa',
        'name_local': 'Hausa'
    },
    'bn': {
        'bidi': False,
        'code': 'bn',
        'name': 'Bengali',
        'name_local': 'বাংলা'
    },
    'my': {
        'bidi': False,
        'code': 'bur_MM',
        'name': 'Burmese',
        'name_local': 'Burmese'
    },
    'ny': {
        'bidi': False,
        'code': 'ny',
        'name': 'Chichewa',
        'name_local': 'Chichewa',
    },
}

LANG_INFO = (
    dict(django.conf.locale.LANG_INFO.items() + EXTRA_LANG_INFO.items()))
django.conf.locale.LANG_INFO = LANG_INFO

LOCALE_PATHS = [
    join(PROJECT_ROOT, "locale"),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'
COMPRESS_ENABLED = True

STATICFILES_STORAGE = (
    'django.contrib.staticfiles.storage.ManifestStaticFilesStorage')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

MEDIA_ROOT = join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

# Wagtail settings

LOGIN_URL = 'molo.profiles:auth_login'
LOGIN_REDIRECT_URL = 'wagtailadmin_home'

SITE_NAME = environ.get('SITE_NAME', "GEM")
WAGTAIL_SITE_NAME = SITE_NAME

ES_HOST = environ.get('ES_HOST')
ES_INDEX = environ.get('ES_INDEX')
ES_VERSION = int(environ.get('ES_VERSION', 5))

ES_BACKEND_V1 = 'wagtail.wagtailsearch.backends.elasticsearch'
ES_BACKEND_V2 = 'wagtail.wagtailsearch.backends.elasticsearch2'
ES_BACKEND_V5 = 'wagtail.wagtailsearch.backends.elasticsearch5'

if ES_VERSION == 5:
    SELECTED_ES_BACKEND = ES_BACKEND_V5
elif ES_VERSION == 2:
    SELECTED_ES_BACKEND = ES_BACKEND_V2
else:
    SELECTED_ES_BACKEND = ES_BACKEND_V1

ES_SELECTED_INDEX = ES_INDEX or environ.get('MARATHON_APP_ID', '')

if ES_HOST and ES_SELECTED_INDEX:
    WAGTAILSEARCH_BACKENDS = {
        'default': {
            'BACKEND': SELECTED_ES_BACKEND,
            'URLS': [ES_HOST],
            'INDEX': ES_SELECTED_INDEX.replace('/', '')
        },
    }


# Whether to use face/feature detection to improve image
# cropping - requires OpenCV
WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = False
IMAGE_COMPRESSION_QUALITY = 85

# This setting lets you override the maximum upload size for images (in bytes).
# If omitted, Wagtail will fall back to using its 10MB default value.
# http://docs.wagtail.io/en/v1.12.2/advanced_topics/settings.html?#maximum-upload-size-for-images

WAGTAILIMAGES_MAX_UPLOAD_SIZE = 1 * 1024 * 1024

ENABLE_SSO = False

# Additional strings that need translations from other modules
# molo.polls
_("Log in to vote")
_("That username already exits. Please try another one.")
_("The old password is incorrect.")
_("Vote")
_("Show Results")
_("You voted: ")
_("Name of the city you were born in")
_("Name of your primary school")
_("Please complete this form to join")

# The `SITE_STATIC_PREFIX` is appended to certain static files in base.html,
# via a templatetag, so that we can use this for different regions:
# Indonesia vs. Rwanda.
# - the site logo
# - style.css
SITE_STATIC_PREFIX = environ.get('SITE_STATIC_PREFIX', '').lower()

GOOGLE_TAG_MANAGER_ACCOUNT = environ.get('GOOGLE_TAG_MANAGER_ACCOUNT')
CUSTOM_UIP_HEADER = 'HTTP_X_IORG_FBS_UIP'

# Password reset - security questions
SECURITY_QUESTION_1 = environ.get(
    'SECURITY_QUESTION_1', 'Name of the city you were born in')
SECURITY_QUESTION_2 = environ.get(
    'SECURITY_QUESTION_2', 'Name of your primary school')


# Comment Filtering Regexes
REGEX_PHONE = r'.*?(\(?\d{3})? ?[\.-]? ?\d{3} ?[\.-]? ?\d{4}.*?'
REGEX_EMAIL = r'([\w\.-]+@[\w\.-]+)'


ADMIN_LANGUAGE_CODE = environ.get('ADMIN_LANGUAGE_CODE', "en")

UNICORE_DISTRIBUTE_API = environ.get(
    'UNICORE_DISTRIBUTE_API', 'http://localhost:6543')
FROM_EMAIL = environ.get('FROM_EMAIL', "support@moloproject.org")
CONTENT_IMPORT_SUBJECT = environ.get(
    'CONTENT_IMPORT_SUBJECT', 'Molo Content Import')

# SMTP Settings
EMAIL_HOST = environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = environ.get('EMAIL_PORT', 25)
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = environ.get(
    'DEFAULT_FROM_EMAIL', 'support@moloproject.org')

GOOGLE_ANALYTICS = {}
GOOGLE_ANALYTICS_IGNORE_PATH = [
    # health check used by marathon
    '/health/',
    # admin interfaces for wagtail and django
    '/admin/', '/django-admin/',
    # Universal Core content import URL
    '/import/',
    # browser troll paths
    '/favicon.ico', '/robots.txt',
    # when using nginx, we handle statics and media
    # but including them here just incase
    '/media/', '/static/',
    # metrics URL used by promethius monitoring system
    '/metrics',
    # REST API
    '/api/',
]

CUSTOM_GOOGLE_ANALYTICS_IGNORE_PATH = environ.get(
    'GOOGLE_ANALYTICS_IGNORE_PATH')
if CUSTOM_GOOGLE_ANALYTICS_IGNORE_PATH:
    GOOGLE_ANALYTICS_IGNORE_PATH += [
        d.strip() for d in CUSTOM_GOOGLE_ANALYTICS_IGNORE_PATH.split(',')]

CSRF_FAILURE_VIEW = 'molo.core.views.csrf_failure'

FREE_BASICS_URL_FOR_CSRF_MESSAGE = environ.get(
    'FREE_BASICS_URL_FOR_CSRF_MESSAGE', 'http://0.freebasics.com/girleffect')


AUTHENTICATION_BACKENDS = [
    'gem.backends.GemModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    'molo.core.backends.MoloCASBackend',
]

AWS_HEADERS = {
    # see http://developer.yahoo.com/performance/rules.html#expires
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}

AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

if AWS_STORAGE_BUCKET_NAME and AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

PWA_SERVICE_WORKER_PATH = join(
    PROJECT_ROOT, 'gem', 'templates', SITE_LAYOUT_BASE, 'serviceworker.js')
PWA_NAME = 'Springster'
PWA_DESCRIPTION = "Springster"
PWA_THEME_COLOR = '#7300FF'
PWA_DISPLAY = 'standalone'
PWA_START_URL = '/'
PWA_ICONS = [
    {
        "src": "/static/img/appicons/springster_icon_96.png",
        "sizes": "96x96",
        "type": "image/png"
    },
    {
        "src": "/static/img/appicons/springster_icon_144.png",
        "sizes": "144x144",
        "type": "image/png"
    },
    {
        "src": "/static/img/appicons/springster_icon_192.png",
        "sizes": "192x192",
        "type": "image/png"
    }
]
PWA_FCM_API_KEY = 'AIzaSyCLtnDpYhzCabuUopYGDLZ4Z-OXRTxdfvg'
PWA_FCM_MSGSENDER_ID = '158972131363'
FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "AAAAJQN6OCM:APA91bFnGtnFFnKcuRZFimMgNCcNzes5QCBvNKVLR"
                      "8NphCN5BhyyVcGxlqNff3ot1mlD-LX_FU2f70Wj6Z-GeHJuJ0QKH2F"
                      "-JMpxsnKb9ljrPqfceJX8eRZujrCVVNFVvp0Gsjyg930o",
    "ONE_DEVICE_PER_USER": True,
    "DELETE_INACTIVE_DEVICES": False,
}

WAGTAILMEDIA_MEDIA_MODEL = 'core.MoloMedia'

# Setup support for proxy headers
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# https://github.com/wagtail/wagtail/issues/3883
AWS_S3_FILE_OVERWRITE = False

PERSONALISATION_SEGMENTS_ADAPTER = 'molo.surveys.adapters.SurveysSegmentsAdapter'
