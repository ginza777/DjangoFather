from .base import *  # noqa

###################################################################
# General
###################################################################

DEBUG = env.bool("DEBUG")

###################################################################
# Django security
###################################################################

"""
IF YOU WANT SET CSRF_TRUSTED_ORIGINS = ["*"] THEN YOU SHOULD SET:
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
"""



CSRF_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = ["https://crm.sherzamon.cloud","http://crm.sherzamon.cloud"]

###################################################################
# CORS
###################################################################

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]
CSRF_COOKIE_HTTPONLY = True




