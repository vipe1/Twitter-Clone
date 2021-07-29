# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from .models import Tweet, Comment, Like
#
# # Create your tests here.
# class TweetsTests(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             username='wojtini',
#             display_name='VIPE',
#             email='test@email.com',
#             password='secret'
#         )
#
#         self.tweet = Tweet.objects.create(
#             author=self.user,
#             content='Interesting content'
#         )
#
#         self.comment = Comment.objects.create(
#             origin=self.tweet,
#             author=self.user,
#             content='Interesting comment'
#         )
#
#         self.like = Like.objects.create(
#             tweet=self.tweet,
#             user=self.user
#         )
#
#     def test_tweet_list_view(self):
#         resp = self.client.get('/')
#         self.assertEqual(resp.status_code, 200)
#         self.assertTemplateUsed(resp, 'tweets/tweet_list.html')
#
#     def test_tweet_content(self):
#         self.assertEqual(self.tweet.author, self.user)
#         self.assertEqual(self.tweet.content, 'Interesting content')
#
#     def test_like(self):
#         like = self.tweet.likes.last()
#         self.assertEqual(like.user, self.user)