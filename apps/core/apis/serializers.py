from rest_framework import serializers

from ..services import VideoService


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoService.model
        fields = '__all__'

