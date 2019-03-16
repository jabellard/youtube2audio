from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urlunparse
from urllib.parse import parse_qs
import youtube_dl


def parse_url(url):
    url = urlparse(url)
    query = parse_qs(url.query)
    query.pop('list', None)
    url = url._replace(query=urlencode(query, True))
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
