import requests
import re
import os

from django.http import StreamingHttpResponse
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework import views
import youtube_dl

from . import serializers
from . import models


class DownloadedVideoListAPIView(ListAPIView):

    serializer_class = serializers.VideoSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return models.Video.objects.none()

        if user.is_superuser:
            return models.Video.objects.all()
        
        return models.Video.objects.filter(downloaded_by_users=user)


class VideoRankingListAPIView(ListAPIView):

    queryset = models.Video.objects.all().order_by('-download_times')[:10]
    serializer_class = serializers.VideoSerializer


class VideoAPIView(views.APIView):

    def fetch_video_info(self, url):
        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})

        with ydl:
            result = ydl.extract_info(url, download=False)

            if 'entries' in result:
                video = result['entries'][0]
            else:
                video = result

            self.video = video
    
    def extract_formats(self, filter_formats=True):
        formats = []
        quality_formats = ['360p', '480p', '720p', '1080p']

        if not filter_formats:
            return self.video.get('formats')

        for _format in self.video.get('formats', []):
            quality_format = _format.get('format_note')
            audio_codec = _format.get('acodec')

            if quality_format not in quality_formats: continue
            if audio_codec == 'none': continue

            formats.append({
                'quality': _format.get('format_note'),
                'url': _format.get('url'),
                'ext': _format.get('ext'),
                'audio_codec': _format.get('acodec'),
            })

        return formats
    
    def get_video_thumbnail_url(self):
        thumbnails = self.video.get('thumbnails', [])
        thumbnail = None

        if thumbnails:
            thumbnail = thumbnails[-1].get('url')

        return thumbnail

    def download_video_thumbnail(self):
        url = self.get_video_thumbnail_url()
        response = requests.get(url)

        if response.status_code == 200:
            title = re.sub("[^0-9a-zA-Z]+", "_", self.video.get('title'))
            title = title.replace(' ', '_')
            
            ext = url.split('.')[-1].split('%')[0].split('?')[0]

            filename = f'{title}.{ext}'
            save_dir = os.path.join('media', 'thumbnails')
            save_path = os.path.join(save_dir, filename)

            if not os.path.isdir(save_dir):
                os.mkdir(save_dir)

            with open(save_path, 'wb') as f:
                f.write(response.content)
                f.close()

            return save_path
        return None

    def stream_video_download(self, url):
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=10000):
                yield chunk
            # yield response.content

    def get_video_dict(self, url):
        formats = self.extract_formats()

        return {
            'url': url,
            'title': self.video.get('title'),
            'thumbnail': self.get_video_thumbnail_url(),
            'formats': formats,
            'channel': self.video.get('channel'),
            'duration': self.video.get('duration')
        }

    def get(self, request):
        url = request.query_params.get('url')
        
        self.fetch_video_info(url)
        video_dict = self.get_video_dict(url)

        return Response(video_dict)

    def post(self, request):
        user = self.request.user
        video_url = request.data.get('video_url', None)
        format_url = request.data.get('format_url', None)
        
        if video_url is None: raise ParseError({'url': 'This field is required'})
        if format_url is None: raise ParseError({'format_url': 'This field is required'})

        self.fetch_video_info(video_url)
        video_dict = self.get_video_dict(video_url)

        thumbnail_url = self.download_video_thumbnail()

        video = models.Video.objects.get_or_create(
            url=video_dict.get('url'),
            title=video_dict.get('title'),
            channel=video_dict.get('channel'),
            duration=video_dict.get('duration'),
        )[0]

        if thumbnail_url:
            video.thumbnail = thumbnail_url.replace('media/', '')

        video.increase_download_times()

        if not user.is_anonymous:
            video.downloaded_by_users.add(user.id)

        return StreamingHttpResponse(self.stream_video_download(format_url))
