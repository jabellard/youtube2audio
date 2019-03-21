import os
import uuid
import subprocess
import shutil
from celery import shared_task
from django.conf import settings
from rest_framework import status
from .settings import MAX_VIDEO_DURATION
from .utils import get_video_info
from .utils import generate_filename
from .utils import TaskError
from .models import Video


# @shared_task(time_limit=300)  # time limit in seconds
@shared_task
def convert(url, audio_format):
    info = get_video_info(url)

    if not info:
        return TaskError(
            {
                'details': 'Invalid URL.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    if info['duration'] > MAX_VIDEO_DURATION:
        return TaskError(
            {
                'details': 'Video duration exceeds {0} minutes.'.format(MAX_VIDEO_DURATION / 60)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    youtube_id = info['id']
    youtube_title = info['title']

    try:
        video = Video.objects.get(youtube_id=youtube_id)
    except Video.DoesNotExist:
        video = Video.objects.create(youtube_id=youtube_id)
    video.title = youtube_title
    video.save()

    audio_filename = generate_filename(youtube_id, audio_format)
    output_filepath = os.path.join(settings.MEDIA_ROOT, audio_filename)

    data = {
        'youtube_id': youtube_id,
        'audio_format': audio_format,
    }

    if os.path.exists(output_filepath):
        return data

    result = _convert(url, audio_filename, audio_format)

    if result == 0:
        return data

    return TaskError(
        {
            'details': 'Internal server error.'
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def _convert(url, audio_filename, audio_format):
    tmp_filepath = os.path.join(settings.MEDIA_ROOT, '{0}_{1}'.format(uuid.uuid4(), audio_filename))
    output_filepath = os.path.join(settings.MEDIA_ROOT, audio_filename)

    try:
        exit_code = subprocess.check_call([
            'youtube-dl',
            '--no-playlist',
            '--extract-audio',
            '--audio-format', audio_format,
            '--output', tmp_filepath,
            url,
        ])
    except subprocess.CalledProcessError as e:
        return e.returncode

    shutil.move(tmp_filepath, output_filepath)

    return exit_code
