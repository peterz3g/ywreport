# coding:utf-8
"""
Django settings for ywreport project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8_qh(fto%mn1x6zbhy)2k+acx^c7i8)ttehlr3amkdp_ysrhj6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chart',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'ywreport.urls'

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

WSGI_APPLICATION = 'ywreport.wsgi.application'

# Database
# PRO_MODEL = "sae"
PRO_MODEL = "local_sqlite3"
# PRO_MODEL = "local_mysql"
# PRO_MODEL = "sae_old_mysql"
# PRO_MODEL = "dao_mysql"

# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
if PRO_MODEL == "sae":
    import sae.const

    # sae.const.MYSQL_DB      # 数据库名
    # sae.const.MYSQL_USER    # 用户名
    # sae.const.MYSQL_PASS    # 密码
    # sae.const.MYSQL_HOST    # 主库域名（可读写）
    # sae.const.MYSQL_PORT    # 端口，类型为<type 'str'>，请根据框架要求自行转换为int
    # sae.const.MYSQL_HOST_S  # 从库域名（只读）
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': sae.const.MYSQL_DB,
            'USER': sae.const.MYSQL_USER,
            'PASSWORD': sae.const.MYSQL_PASS,
            'HOST': sae.const.MYSQL_HOST,
            'PORT': sae.const.MYSQL_PORT,
        }
    }
elif PRO_MODEL == 'sae_old_mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'app_peterz3g001',
            'USER': '1402y03l5j',
            'PASSWORD': '0kw001zx055ilij1hwwjmhizj32j5h0lxlm5xk50',
            'HOST': 'w.rdc.sae.sina.com.cn',
            'PORT': '3307',
        }
    }
elif PRO_MODEL == 'local_sqlite3':
    DATABASES = {
        'default': {
            # for local sqllite connect
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
elif PRO_MODEL == 'dao_mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'sr0BNEXuIAtQhmMV',
            'USER': 'uFZdPMiIBbnO2cCW',
            'PASSWORD': 'pHahMksnmIrpwlY1N',
            'HOST': '10.10.26.58',
            'PORT': '3306',
        }
    }

elif PRO_MODEL == 'local_mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            # for local mysql connect
            'NAME': 'app_peterz3g',
            'USER': 'peterz3g',
            'PASSWORD': '123456',
            'HOST': '192.168.124.131',
            'PORT': '3306',
        }
    }

# from sae._restful_mysql import monkey
# monkey.patch()

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    #    os.path.join(BASE_DIR, "common_static"),
)

# the crontab jobs
# LOG_DIR = os.path.join(BASE_DIR, 'log')
# CRONJOBS = [
#     ('*/1 * * * *', 'chart.batTasks.timerTasks.impFiles2DB', '>> %s' % os.path.join(LOG_DIR, 'impFiles2DB.log')),
#     ('16 5 * * *', 'chart.batTasks.timerTasks.dbImpFromFiles', '>> %s' % os.path.join(LOG_DIR, 'dbImpFromFiles.log'))
# ]
