from django.urls import path
from .views import TweetListAPIView, TweetDetailAPIView, \
    AuthorListAPIView, AuthorTweetsAPIView

urlpatterns = [
    path('posts/', TweetListAPIView.as_view()),
    path('posts/<int:pk>', TweetDetailAPIView.as_view()),


    path('authors', AuthorListAPIView.as_view()),
    path('authors/<int:pk>', AuthorTweetsAPIView.as_view()),
]