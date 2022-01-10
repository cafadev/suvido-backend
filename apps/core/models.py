from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Video(models.Model):

    title = models.CharField(max_length=255)
    url = models.TextField()
    downloaded_by_users = models.ManyToManyField(User)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True)
    download_times = models.PositiveIntegerField(default=0)
    channel = models.CharField(max_length=255)
    duration = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def increase_download_times(self):
        self.download_times += 1
        self.save()
