import requests
import re
import os
import youtube_dl

from apps.common.base import BaseService
from .models import Video

class VideoService(BaseService):

    model = Video

    @staticmethod
    def save(video, *args, **kwargs):
        video.save(**kwargs)

    @staticmethod
    def increase_download_times(video: Video, *args, **kwargs):
        video.download_times += 1

    @staticmethod
    def get_top_videos():
        return VideoService.get_active_records().order_by('-download_times')[:10]
    
    @staticmethod
    def fetch_video_info(url):
        ydl = youtube_dl.YoutubeDL({})

        with ydl:
            result = ydl.extract_info(url, download=False)

            if 'entries' in result:
                video = result['entries'][0]
            else:
                video = result

            return video
    
    @staticmethod
    def extract_formats(video, filter_formats=True):
        formats = []
        quality_formats = ['360p', '480p', '720p', '1080p']

        if not filter_formats:
            return video.get('formats')

        for _format in video.get('formats', []):
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
    
    @staticmethod
    def get_video_thumbnail_url(video):
        thumbnails = video.get('thumbnails', [])
        thumbnail = None

        if thumbnails:
            thumbnail = thumbnails[-1].get('url')

        return thumbnail

    @staticmethod
    def download_video_thumbnail(video):
        url = VideoService.get_video_thumbnail_url(video)
        response = requests.get(url)

        if response.status_code == 200:
            title = re.sub("[^0-9a-zA-Z]+", "_", video.get('title'))
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

    @staticmethod
    def stream_video_download(url):
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=10000):
                yield chunk

    @staticmethod
    def get_video_dict(video, url):
        formats = VideoService.extract_formats(video)

        return {
            'url': url,
            'title': video.get('title'),
            'thumbnail': VideoService.get_video_thumbnail_url(video),
            'formats': formats,
            'channel': video.get('channel'),
            'duration': video.get('duration')
        }
    
    @staticmethod
    def get_or_create(video):
        _video = Video.objects.get_or_create(
            url=video.get('url'),
            title=video.get('title'),
            channel=video.get('channel'),
            duration=video.get('duration'),
        )[0]
        return _video[0]
    
    @staticmethod
    def add_user_to_downloads(user, video):
        if not user.is_anonymous:
            video.downloaded_by_users.add(user.id)

    @staticmethod
    def get_video_downloads_by_user(user):
        if user.is_anonymous:
            return Video.objects.none()

        if user.is_superuser:
            return Video.objects.all()
        
        return VideoService.get_active_records(downloaded_by_users=user)
