from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """ Tells Django to put static files in the location defined in settings """
    location = settings.STATICFILES_LOCATION
