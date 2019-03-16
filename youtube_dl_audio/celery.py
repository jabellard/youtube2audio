import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_dl_audio.settings.base')

app = Celery('youtube_dl_audio')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)
