from django.conf.urls import url
from django.urls import include
from django.urls import path
from .views import Admin


urlpatterns = [
    url(r'^$', Admin.as_view(), name='_admin'),
]
