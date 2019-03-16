from django.conf.urls import url
from django.urls import include
from django.urls import path

from .views import Convert
from .views import CheckConversionStatus
from .views import Download

urlpatterns = [
    url(r'^convert/$',
        Convert.as_view(), name='convert'),
    url(r'^check_conversion_status/(?P<task_id>[0-9a-f-]+)/$',
        CheckConversionStatus.as_view(), name='check_conversion_status'),
    url(r'^download/(?P<youtube_id>\w{11})/(?P<audio_format>\w{1,10})/$',
        Download.as_view(), name='download'),
]
