from django.urls import path, include
from .views import \
    TweetListView, TweetCreateView, TweetLikeView,\
    TweetDetailView, TweetEditView, TweetDeleteView,\
    TweetBookmarkView, BookmarkListView, TweetCommentView, \
    TweetRetweetView, CommentDeleteView

urlpatterns = [
    path('', TweetListView.as_view(), name='tweet_list'),
    path('tweet/create/', TweetCreateView.as_view(), name='tweet_create'),
    path('tweet/<int:pk>/', include([
        path('', TweetDetailView.as_view(), name='tweet_detail'),
        path('comments', TweetCommentView.as_view(), name='tweet_comments'),

        path('edit', TweetEditView.as_view(), name='tweet_edit'),
        path('delete', TweetDeleteView.as_view(), name='tweet_delete'),

        path('like', TweetLikeView.as_view(), name='tweet_like'),
        path('retweet', TweetRetweetView.as_view(), name='tweet_retweet'),
        path('bookmark', TweetBookmarkView.as_view(), name='tweet_bookmark'),
    ])),

    path('comment/<int:pk>/delete', CommentDeleteView.as_view(), name='comment_delete'),
    path('bookmarks/', BookmarkListView.as_view(), name='bookmark_list'),
]