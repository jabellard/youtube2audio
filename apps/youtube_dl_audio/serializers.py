from rest_framework import serializers


class VideoConvertSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)
    audio_format = serializers.CharField(required=True)

    class Meta:
        pass
