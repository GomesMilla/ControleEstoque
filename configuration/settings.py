from pathlib import Path
import os, sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_ff#=83@scebs%+$+_@n$v+_x8=l%9r3kzlryat+)+-=l*lv38'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

sys.path.append(
    os.path.join(BASE_DIR, "apps")
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'colorfield',
    'ckeditor',
    'ckeditor_uploader',
    'bootstrapform',
    'django_select2',
]

INSTALLED_APPS += [
    'core',
    'users',
    'agenda',
]

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'skin': "moono-lisa",
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['NumberedList', 'BulletedList', 'Print', 'Outdent', 'Indent', '-', 'JustifyLeft', 
            'JustifyCenter', 'JustifyRight', 'JustifyBlock','RemoveFormat', 'SelectAll','Maximize','Strike','Select','Save'],
            
            ['Cut', 'Copy', 'Paste', 'Undo', 'Redo','Bold', 'Italic', 'Underline','Image','Link',
            'Unlink','TextColor', 'BGColor','Find','Preview','NewPage','PageBreak','a11yhelp','Table','About'],
            
            ['Styles', 'Format', 'Font', 'FontSize'],
        ],'width': '100%'
    },
    'DescricaoServico': {
        'skin': "moono-lisa",
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['NumberedList', 'BulletedList', 'Print', 'Outdent', 'Indent', 'color', 'JustifyLeft', 
            'JustifyCenter', 'JustifyRight', 'JustifyBlock','RemoveFormat', 'SelectAll','Maximize','Strike','Select','Save'],
            
            ['Cut', 'Copy', 'Paste', 'Undo','Redo','Bold', 'Italic', 'Underline','','Link',
            'Unlink','TextColor', 'BGColor','Find','Preview','NewPage','PageBreak','a11yhelp','Table','About'],
            
            ['Styles', 'Format', 'Font', 'FontSize'],
        ],'width': '100%'
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'configuration.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'users.views.base'
            ],
        },
    },
]

WSGI_APPLICATION = 'configuration.wsgi.application'
AUTH_USER_MODEL = "users.User" 
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL='/media/'
MEDIA_ROOT='media/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
