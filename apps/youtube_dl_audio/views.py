from rest_framework import generic
from django.utils.encoding import smart_str
from rest_framework.response import Response
from rest_framework import status
from .models import Video
from .serializers import VideoConvertSerializer
from .settings import ALLOWED_AUDIO_FORMATS
from .utils import parse_url
from .tasks import convert


class Convert(generics.CreateAPIView):
    serializer_class = VideoConvertSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.data['audio_format'] in ALLOWED_AUDIO_FORMATS:
            return Response(
                {
                    'detail': 'Invalid audio format.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        url = parse_url(request.data['url'])

        task = convert.delay(url)

        return Response(
            {
                'task_id': task.task_id
            },
            status=status.HTTP_200_OK
        )


class CheckConversionStatus(generics.RetrieveAPIView):
    serializer_class = None

    def get(self, request, *args, **kwargs):
        task_id = self.kwargs['task_id']
        task_result = AsyncResult(tast_id)

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

        if isinstance(task_result, Response):
            return task_result

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
    serializer_class = None

    def get(self, request, *args, **kwargs):
        file_name = '{0}.{1}'.format(self.kwargs['youtube_id'], self.kwargs['audio_format'])
        filepath = os.path.join(settings.MEDIA_ROOT, file_name)
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
                                                    smart_str(file_name))
        return response
