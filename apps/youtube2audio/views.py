import os
from rest_framework import generics
from django.conf import settings
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from .models import Video
from .serializers import VideoConvertSerializer
from .settings import ALLOWED_AUDIO_FORMATS
from .utils import parse_url
from .utils import TaskError
from .utils import get_video_info
from .tasks import convert
from celery.result import AsyncResult


class Convert(generics.CreateAPIView):
    serializer_class = VideoConvertSerializer
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        audio_format = request.data['audio_format']
        if not audio_format in ALLOWED_AUDIO_FORMATS:
            return Response(
                {
                    'detail': 'Invalid audio format.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        url = parse_url(request.data['url'])

        task = convert.delay(url, audio_format)

        conversion_status_link = reverse(
            'check_conversion_status',
            kwargs={
                'task_id': task.id
            }
        )

        return Response(
            {
                'conversion_status_link': conversion_status_link
            },
            status=status.HTTP_200_OK
        )


class CheckConversionStatus(generics.RetrieveAPIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        task_id = self.kwargs['task_id']
        task_result = AsyncResult(task_id)

        data = {
            'task_id': task_id,
            'executed': False,
            'successful': None,
            'download_link': None
        }

        if not task_result.ready():
            return Response(
                data,
                status=status.HTTP_200_OK
            )

        if not task_result.successful():
            return Response(
                {
                    'details': 'Internal server error.'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        task_result = task_result.result

        if isinstance(task_result, TaskError):
            return Response(
                task_result.data,
                task_result.status
            )

        data['executed'] = True
        data['successful'] = True

        download_link = reverse(
            'download',
            kwargs={
                'youtube_id': task_result['youtube_id'],
                'audio_format': task_result['audio_format'],
            }
        )
        data['download_link'] = download_link

        return Response(
            data,
            status=status.HTTP_200_OK
        )


class Download(generics.RetrieveAPIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        youtube_id = self.kwargs['youtube_id']
        audio_format = self.kwargs['audio_format']
        filename = '{0}.{1}'.format(youtube_id, audio_format)
        filepath = os.path.join(settings.MEDIA_ROOT, filename)
        file_exists = os.path.exists(filepath)

        if not file_exists:
            return Response(
                {
                    'details': 'Not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        with open(filepath, 'rb') as audio_file:
            response = HttpResponse(audio_file.read(), content_type='audio/*')

        try:
            video = Video.objects.get(youtube_id=youtube_id)
        except Video.DoesNotExist:
            video = Video.objects.create(youtube_id=youtube_id)

        url = 'https://www.youtube.com/watch?v=' + youtube_id
        info = get_video_info(url)
        download_filename = filename
        if info:
            title = info['title']
            download_filename = '{0}.{1}'.format(title, audio_format)
            video.title = title

        video.download_count += 1
        video.save()

        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            smart_str(download_filename))
        response['Content-Length'] = os.path.getsize(filepath)
        return response
