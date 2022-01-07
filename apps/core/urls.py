from django.urls import path
from . import views


urlpatterns = [
    path('api/videos/me/', views.DownloadedVideoListAPIView.as_view()),
    path('api/videos/', views.VideoAPIView.as_view()),
    path('api/ranking/', views.VideoRankingListAPIView.as_view())
]
