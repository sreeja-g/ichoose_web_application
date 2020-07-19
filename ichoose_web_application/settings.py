"""
Django settings for ichoose_web_application project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$f#=^@-m3)6i+@u6-$8x5qdo0xav8q_3j0#q((apb4%n6h@e5m'

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
    'registration.apps.RegistrationConfig',
    'social_django',
    'ichoose',
    'isell',
    'ilend',
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

ROOT_URLCONF = 'ichoose_web_application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'ichoose_web_application.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'


#-------------------------non default-----------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'ichoose_web_app_db',
        'Host':'mongodb://127.0.0.1:27017/',
    }
}

AUTH_USER_MODEL = 'registration.User'

#--------------------------O-auth-------------------------------

AUTHENTICATION_BACKENDS = (
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1098294132267-7igddfho82ldmf271rr2duc4tom277q6.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'mZ89eXlN5wTfBqqiw4ozNNL7'

SOCIAL_AUTH_FACEBOOK_KEY = '184350956171545'
SOCIAL_AUTH_FACEBOOK_SECRET = '4f187d2c1b927ac0b7d8ceeb2da79793'

SOCIAL_AUTH_TWITTER_KEY = 'yzSJx9h2b9t93h9kKBqa4zDsG'
SOCIAL_AUTH_TWITTER_SECRET = 'N5ttuX7jPgclPwEuYhgf8EHAJTpzaz7JTn4vGl8yLkVBnCg02u'

LOGIN_URL = '/auth/login/google-oauth2/'

LOGIN_REDIRECT_URL = 'registration:home'
LOGOUT_REDIRECT_URL = 'registration:logout'

SOCIAL_AUTH_URL_NAMESPACE = 'social'

#-------------------------email------------------

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_HOST_USER = 'aselib123@gmail.com'
EMAIL_HOST_PASSWORD = 'Project@12'
EMAIL_PORT = 587

#______________________________media______________________
MEDIA_ROOT=os.path.join(BASE_DIR,'media')
MEDIA_URL='/media/'


STRIPE_PUBLISHABLE_KEY = 'pk_test_6PfPJERL0M0vDU2MVtjvQ79M00xOYHX6rv'
STRIPE_SECRET_KEY = 'sk_test_3i8WhDyjrlXAyeNjusezESCd00eJQ3ewpJ'