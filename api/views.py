from rest_framework import generics
from tweets.models import Tweet
from .serializers import TweetSerializer

# Create your views here.
class TweetListAPIView(generics.ListAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

class TweetDetailAPIView(generics.RetrieveAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
