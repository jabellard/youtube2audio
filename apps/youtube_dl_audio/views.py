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

        return Response(
            {
                'task_id': task.id
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
        filename = '{0}.{1}'.format(self.kwargs['youtube_id'], self.kwargs['audio_format'])
        filepath = os.path.join(settings.MEDIA_ROOT, filename)
        file_exists = os.path.exists(filepath)

        if not file_exists:
            return Response(
                {
                    'details': 'Not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        response = HttpResponse(content_type='application/force-download')
        response['Content-Length'] = os.path.getsize(filepath)
        response['X-Accel-Redirect'] = os.path.join(settings.MEDIA_URL,
                                                    smart_str(filename))
        return response
