from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .serializers import CommandSerializer
from .settings import COMMANDS


class Admin(generics.UpdateAPIView):
    serializer_class = CommandSerializer
    permission_classes = (IsAdminUser,)

    '''

   def get(self, request, *args, **kwargs):
        return Response(
            {
                'detail': 'Not implemented.'
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )
    '''

    def update(self, request, *args, **kwargs):
        self.serializer_class = CommandSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cmd = request.data['cmd']

        if cmd in COMMANDS:
            handler = COMMANDS[cmd]
            return handler()
        else:
            return Response(
                {
                    'detail': 'Invalid command.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
