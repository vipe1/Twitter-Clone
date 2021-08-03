from rest_framework import generics
from django.contrib.auth import get_user_model
from tweets.models import Tweet
from .serializers import TweetSerializer, AuthorSerializer

# Create your views here.
class TweetListAPIView(generics.ListAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer


class TweetDetailAPIView(generics.RetrieveAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer


class AuthorListAPIView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = AuthorSerializer


class AuthorTweetsAPIView(generics.RetrieveAPIView):
    queryset = get_user_model()
    serializer_class = AuthorSerializer