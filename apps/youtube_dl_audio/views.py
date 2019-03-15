from rest_framework import generics
from .models import Video
from .serializers import VideoConvertSerializer
from .settings import ALLOWED_AUDIO_FORMATS
from .utils import parse_url


class Convert(generics.CreateAPIView):
    serializer_class = VideoConvertSerializer

    def post_checks(self, request, *args, **kwargs):
        return None

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

        return task_result.result


class Download(generics.RetrieveAPIView):
    serializer_class = None

    def get(self, request, *args, **kwargs):
        pass
