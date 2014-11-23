#coding:utf-8
"""
Django settings for doctor project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__)).decode('gbk')
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jjg&@7&&wqa(&$!396om49d851+ix&t65e3#0c_5i!t^15p3u1'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
#TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

TEMPLATE_DIRS = (
        os.path.join(BASE_DIR, 'doctor/template') ,
        )



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'doctor',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'doctor.urls'

WSGI_APPLICATION = 'doctor.wsgi.application'

# 线上数据库的配置
try:
    import sae.const
    from sae.const import (
         MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
     )
    ENGINE = 'django.db.backends.mysql'
except:
    ENGINE = 'django.db.backends.sqlite3'
    MYSQL_HOST = ''
    MYSQL_PORT = ''
    MYSQL_USER = ''
    MYSQL_PASS = ''
    MYSQL_DB = os.path.join(BASE_DIR, 'question.db')
#
    #ENGINE = 'django.db.backends.mysql'
    #MYSQL_HOST = '127.0.0.1'
    #MYSQL_PORT = '3306'
    #MYSQL_USER = 'root'
    #MYSQL_PASS = ''
    #MYSQL_DB = 'question'


DATABASES = {
    'default': {
        'ENGINE':   ENGINE,
        'NAME':     MYSQL_DB,
        'USER':     MYSQL_USER,
        'PASSWORD': MYSQL_PASS,
        'HOST':     MYSQL_HOST,
        'PORT':     MYSQL_PORT,
    }
}   

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'doctor/static/'),
    )

EMAIL_USE_TLS =True
EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST_USER = 'dhs789520@163.com'
EMAIL_HOST_PASSWORD = 'dhs2ksingle'
EMAIL_PORT = 25

