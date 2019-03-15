from django.conf.urls import url
from django.urls import include
from django.urls import path

from .views import Convert
from .views import CheckConversionStatus
from .views import Download

urlpatterns = [
    url(r'^convert/$',
        Convert.as_view(), name='convert'),
    url(r'^check_conversion_status/(?P<task_id>\w{8})/$',
        CheckConversionStatus.as_view(), name='check_conversion_status'),
    url(r'^download/(?P<file_name>\w{8})/$',
        CheckConversionStatus.as_view(), name='download'),
]
