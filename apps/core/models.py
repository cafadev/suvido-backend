from django.db import models
from django.contrib.auth import get_user_model

from apps.common.base import BaseModel

User = get_user_model()

class Video(BaseModel):

    title = models.CharField(max_length=255)
    url = models.TextField()
    downloaded_by_users = models.ManyToManyField(User)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True)
    download_times = models.PositiveIntegerField(default=0)
    channel = models.CharField(max_length=255)
    duration = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
