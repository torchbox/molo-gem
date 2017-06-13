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

    'molo.core',
    'gem',
    'gem.personalise',
    'molo.profiles',
    'molo.surveys',
    'django_comments',
    'molo.commenting',
    'molo.yourwords',
    'molo.servicedirectory',
    'molo.polls',
    'mote',
    'gem.csv_group_creation',

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
    'wagtailsurveys',
    'wagtail.contrib.wagtailsitemaps',

    'wagtail_personalisation',
    'wagtailfontawesome',

    'mptt',
    'django.contrib.sites',
    'google_analytics',

    'raven.contrib.django.raven_compat',
    'djcelery',
    'django_cas_ng',
    'compressor',
    'notifications',
    'el_pagination',

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

    'molo.core.middleware.MoloGoogleAnalyticsMiddleware',
    'molo.core.middleware.MultiSiteRedirectToHomepage',
]

# Template configuration

# We have multiple layouts: use `base`, `malawi` or `springster`
# to switch between them.
SITE_LAYOUT_BASE = environ.get('SITE_LAYOUT_BASE', 'base')
SITE_LAYOUT_2 = environ.get('SITE_LAYOUT_2', '')

TEMPLATES = [
    {
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
                'gem.processors.compress_settings',
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "mote.loaders.app_directories.Loader",
                "django.template.loaders.app_directories.Loader",
            ]
        },
    },
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
        'schedule': crontab(minute='*'),
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

# Use Elasticsearch as the search backend for extra performance and better
# search results:
# http://wagtail.readthedocs.org/en/latest/howto/performance.html#search
# http://wagtail.readthedocs.org/en/latest/core_components/
#     search/backends.html#elasticsearch-backend
#
# WAGTAILSEARCH_BACKENDS = {
#     'default': {
#         'BACKEND': ('wagtail.wagtailsearch.backends.'
#                     'elasticsearch.ElasticSearch'),
#         'INDEX': 'base',
#     },
# }


# Whether to use face/feature detection to improve image
# cropping - requires OpenCV
WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = False
IMAGE_COMPRESSION_QUALITY = 85

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
]

CUSTOM_GOOGLE_ANALYTICS_IGNORE_PATH = environ.get(
    'GOOGLE_ANALYTICS_IGNORE_PATH')
if CUSTOM_GOOGLE_ANALYTICS_IGNORE_PATH:
    GOOGLE_ANALYTICS_IGNORE_PATH += [
        d.strip() for d in CUSTOM_GOOGLE_ANALYTICS_IGNORE_PATH.split(',')]

CSRF_FAILURE_VIEW = 'molo.core.views.csrf_failure'

FREE_BASICS_URL_FOR_CSRF_MESSAGE = environ.get(
    'FREE_BASICS_URL_FOR_CSRF_MESSAGE', 'http://0.freebasics.com/girleffect')
