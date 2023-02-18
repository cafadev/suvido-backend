from django.urls import path
from .apis import rest


urlpatterns = [
    path('', rest.VideoAPI.as_view()),
    path('me/', rest.DownloadedVideoAPI.as_view()),
    path('ranking/', rest.RankAPI.as_view())
]
