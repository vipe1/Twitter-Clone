from django.urls import path
from .views import TweetListAPIView, TweetDetailAPIView

urlpatterns = [
    path('posts/', TweetListAPIView.as_view()),
    path('posts/<int:pk>', TweetDetailAPIView.as_view())
]