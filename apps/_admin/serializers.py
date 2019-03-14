'''
from rest_framework import serializers


class CommandSerializer(serializers.Serializer):
    cmd = serializers.CharField(required=True)
'''
