import copy

from .common import *
from .partials.util import get_secret
from djangoplicity.contentserver import CDN77ContentServer

# Make this unique, and don't share it with anybody.
SECRET_KEY = "sssmvx$i1sv4k*g+nwfnx*3a1g&)^i6r9n6g4=f_$x^u(kwt8s"

DATABASES = copy.deepcopy(DATABASES)
DATABASES['default']['HOST'] = ""
DATABASES['default']['PASSWORD'] = ""


EMAIL_HOST = 'smtphost.hq.eso.org'
EMAIL_PORT = '25'
EMAIL_SUBJECT_PREFIX = '[WEBB-INTEGRATION]'


CELERY_BROKER_URL = ''


# Shop:
ORDER_PREFIX = "hbi"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'KEY_PREFIX': 'nova',
        'LOCATION': [
            '',
        ],
        'TIMEOUT': 86400
    },
}

MEDIA_CONTENT_SERVERS = {
    'CDN77': CDN77ContentServer(
        name='CDN77',
        formats={
            'djangoplicity.media.models.images.Image': (
                'large',
                'publicationjpg',
                'screen',
                'wallpaper1',
                'wallpaper2',
                'wallpaper3',
                'wallpaper4',
                'wallpaper5',
                'thumb150y',
                'thumb300y',
                'thumb350x',
                'thumb700x',
                'newsfeature',
                'news',
                'banner1920',
                'screen640',
                'zoomable',
            ),
            'djangoplicity.media.models.videos.Video': (
                'videoframe',
                'small_flash',
                'medium_podcast',
                'medium_mpeg1',
                'medium_flash',
                'large_qt',
                'broadcast_sd',
                'hd_and_apple',
                'hd_broadcast_720p50',
                'hd_1080p25_screen',
                'hd_1080p25_broadcast',
                'ultra_hd',
                'ultra_hd_h265',
                'ultra_hd_broadcast',
                'dome_8kmaster',
                'dome_4kmaster',
                'dome_2kmaster',
                'dome_mov',
                'dome_preview',
                'cylindrical_4kmaster',
                'cylindrical_8kmaster',
                'cylindrical_16kmaster',
                'news',
                'qhd_1440p25_screen',
                '8k_4320p25_screen',
                'm_hd_1080p_screen',
                'm_ultra_hd_screen',
            ),
        },
        url='https://cdn.esawebb.org/',
        url_bigfiles='https://cdn2.esawebb.org/',
        remote_dir='',
        host='push-12.cdn77.com',
        username=get_secret('CDN_STORAGE_USERNAME'),
        password=get_secret('CDN_STORAGE_PASSWORD'),
        api_login=get_secret('CDN_API_LOGIN'),
        api_password=get_secret('CDN_API_PASSWORD'),
        cdn_id='1495410064',
        cdn_id_bigfiles='1084865783',
        aws_access_key_id=get_secret('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=get_secret('AWS_SECRET_ACCESS_KEY'),
        aws_storage_bucket_name=get_secret('AWS_STORAGE_BUCKET_NAME'),
        aws_s3_region_name=get_secret('AWS_S3_REGION_NAME'),
        aws_s3_endpoint_url=get_secret('AWS_S3_ENDPOINT_URL'),
        aws_s3_custom_domain=get_secret('AWS_S3_CUSTOM_DOMAIN')
    ),
}
