from rest_framework.response import Response
from rest_framework import status


def execute_delete_old_audio_files(api=True):
    return Response(
        {
            'detail': 'Not implemented.'
        },
        status=status.HTTP_200_OK
    )
