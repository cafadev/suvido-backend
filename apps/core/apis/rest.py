
from django.http import StreamingHttpResponse
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework import views

from .serializers import VideoSerializer
from ..services import VideoService


class DownloadedVideoAPI(ListAPIView):

    serializer_class = VideoSerializer

    def get_queryset(self):
        return VideoService.get_video_downloads_by_user(self.request.user)


class RankAPI(ListAPIView):

    queryset = VideoService.get_top_videos()
    serializer_class = VideoSerializer


class VideoAPI(views.APIView):

    def get(self, request):
        video_url = request.query_params.get('video_url')
        
        video = VideoService.fetch_video_info(video_url)
        video_dict = VideoService.get_video_dict(video, video_url)

        return Response(video_dict)

    def post(self, request):
        video_url = request.data.get('video_url', None)
        format_url = request.data.get('format_url', None)
        
        if video_url is None: raise ParseError({'url': 'This field is required'})
        if format_url is None: raise ParseError({'format_url': 'This field is required'})

        video = VideoService.fetch_video_info(video_url)
        video_dict = VideoService.get_video_dict(video, video_url)
        thumbnail_url = VideoService.download_video_thumbnail(video)
        video = VideoService.get_or_create(video_dict)

        if thumbnail_url:
            video.thumbnail = thumbnail_url.replace('media/', '')

        VideoService.add_user_to_downloads(request.user, video)
        VideoService.increase_download_times(video)
        VideoService.save(video)

        return StreamingHttpResponse(VideoService.stream_video_download(format_url))
