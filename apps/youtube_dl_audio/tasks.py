from celery import shared_task
from rest_framework.response import Response
from rest_framework import status
from .settings import MAX_VIDEO_DURATION
from .utils import get_video_info


@shared_task(time_limit=300)
def convert(url, audio_format):
    info = get_video_info(url)

    if not info:
        return Response(
            {
                'details': 'Internal server error.'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    if info['duration'] > MAX_VIDEO_DURATION:
        return Response(
            {
                'details': 'Internal server error.'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    audio_filename = generate_filename(info['id'], audio_format)
    output_filepath = os.path.join(settings.MEDIA_ROOT, audio_filename)

    data = {
        'youtube_id': info['id'],
        'audio_format': audio_format,
    }

    if os.path.exists(output_filepath):
        return data

    result = _convert(url, audio_filename, audio_format)

    if result == 0:
        return data

    return Response(
        {
            'details': 'Internal server error.'
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def _convert(url, audio_filename, audio_format):
    tmp_filepath = os.path.join(settings.MEDIA_ROOT, '{0}_{1}'.format(uuid.uuid4(), audio_filename))
    output_filepath = os.path.join(settings.MEDIA_ROOT, audio_filename)

    exit_code = subprocess.check_call([
        'youtube-dl',
        '--no-playlist',
        '--extract-audio',
        '--audio-format', audio_format,
        '--output', tmp_filepath,
        '--cache-dir', '/tmp/youtube_dl',
        url,
    ])

    if exit_code == 0:
        shutil.move(tmp_filepath, output_filepath)

    return exit_code
