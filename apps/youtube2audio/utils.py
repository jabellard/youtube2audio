from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urlunparse
from urllib.parse import parse_qs
from rest_framework import status
import youtube_dl


def parse_url(url):
    query = parse_qs(urlparse(url).query)

    if 'list' in query:
        query.pop('list')
        url = url._replace(query=urlencode(query, True))
        url = urlunparse(url)
        return url

    return url


def get_video_info(url):
    ydl = youtube_dl.YoutubeDL({'noplaylist': True})
    ydl.add_default_info_extractors()

    try:
        info = ydl.extract_info(url, download=False)
        return info
    except Exception:
        return None


def generate_filename(youtube_id, audio_format):
    return '{0}.{1}'.format(youtube_id, audio_format)


class TaskError:
    def __init__(self, data={'details': 'OK.'}, status=status.HTTP_200_OK):
        self.data = data
        self.status = status
