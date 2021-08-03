from django.urls import path
from .views import \
    TweetListView, TweetCreateView, TweetLikeView,\
    TweetDetailView, TweetEditView, TweetDeleteView,\
    TweetBookmarkView, BookmarkListView, TweetCommentView, \
    TweetRetweetView, CommentDeleteView

urlpatterns = [
    path('', TweetListView.as_view(), name='tweet_list'),
    path('tweet/create/', TweetCreateView.as_view(), name='tweet_create'),
    path('tweet/<int:pk>/', TweetDetailView.as_view(), name='tweet_detail'),
    path('tweet/<int:pk>/comments', TweetCommentView.as_view(), name='tweet_comments'),
    path('comment/<int:pk>/delete', CommentDeleteView.as_view(), name='comment_delete'),

    path('tweet/<int:pk>/edit', TweetEditView.as_view(), name='tweet_edit'),
    path('tweet/<int:pk>/delete', TweetDeleteView.as_view(), name='tweet_delete'),
    path('tweet/<int:pk>/like/', TweetLikeView.as_view(), name='tweet_like'),
    path('tweet/<int:pk>/retweet/', TweetRetweetView.as_view(), name='tweet_retweet'),

    path('tweet/<int:pk>/bookmark/', TweetBookmarkView.as_view(), name='tweet_bookmark'),
    path('bookmarks/', BookmarkListView.as_view(), name='bookmark_list'),
]