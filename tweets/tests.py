from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from .models import Tweet, Comment, Like, Bookmark
from accounts.models import CustomUser
from .forms import TweetCreateForm, CommentCreateForm

# Create your tests here.
class TweetsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='wojtini',
            display_name='VIPE',
            email='test@email.com',
            password='secret'
        )
        self.client.login(username='wojtini', password='secret')

        self.user2 = get_user_model().objects.create_user(
            username='andrzej',
            display_name='NRB',
            email='test2@email.com',
            password='secret2'
        )

        self.tweet = Tweet.objects.create(
            author=self.user,
            content='Interesting content'
        )

        self.comment = Comment.objects.create(
            origin=self.tweet,
            author=self.user,
            content='Interesting comment'
        )

        self.like = Like.objects.create(
            tweet=self.tweet,
            user=self.user
        )

        self.bookmark = Bookmark.objects.create(
            tweet=self.tweet,
            user=self.user2
        )


    def test_user_model(self):
        self.assertIsInstance(self.user, CustomUser)
        self.assertIsInstance(self.user2, CustomUser)


    def test_non_logged_access(self):
        self.client.logout()
        resp = self.client.get(reverse('tweet_list'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=/')


    def test_tweet_list_view(self):
        resp = self.client.get(reverse('tweet_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'tweets/tweet_list.html')


    def test_tweet_content(self):
        self.assertEqual(self.tweet.author, self.user)
        self.assertEqual(self.tweet.content, 'Interesting content')


    def test_comment_content(self):
        comment = self.tweet.comments.last()
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, 'Interesting comment')


    def test_like(self):
        like = self.tweet.likes.last()
        self.assertEqual(like.user, self.user)


    def test_bookmark(self):
        bookmark = self.user2.bookmarks.last()
        self.assertEqual(bookmark.tweet, self.tweet)


    def test_tweet_create_form(self):
        dummy_data = {
            'content': 'dum dum text'
        }
        form = TweetCreateForm(data=dummy_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['content'], 'dum dum text')


    def test_tweet_create_form_with_user(self):
        dummy_data = {
            'author': self.user,
            'content': 'dum dum text'
        }
        form = TweetCreateForm(data=dummy_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['content'], 'dum dum text')
        # Check if form accepted author data, which is not supposed to be there
        try:
            form.cleaned_data['author']
        except KeyError:
            pass
        else:
            raise self.fail('''Author field shouldn't be accepted in this form''')


    def test_tweet_with_too_long_content(self):
        test_string = 'b' * 501
        dummy_data = {
            'author': self.user2,
            'content': test_string
        }
        form = TweetCreateForm(data=dummy_data)
        self.assertFalse(form.is_valid())


    def test_comment_create_form(self):
        dummy_data = {
            'origin': self.tweet,
            'author': self.user2,
            'content': 'dum dum comment text'
        }
        form = CommentCreateForm(data=dummy_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['content'], 'dum dum comment text')


    def test_comment_create_form_with_user(self):
        dummy_data = {
            'author': self.user2,
            'content': 'dum dum comment text'
        }
        form = CommentCreateForm(data=dummy_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['content'], 'dum dum comment text')
        # Check if form accepted author data, which is not supposed to be there
        try:
            form.cleaned_data['author']
        except KeyError:
            pass
        else:
            raise self.fail('''Author field shouldn't be accepted in this form''')


    def test_comment_with_too_long_content(self):
        test_string = 'b' * 101
        dummy_data = {
            'origin': self.tweet,
            'author': self.user2,
            'content': test_string
        }
        form = CommentCreateForm(data=dummy_data)
        self.assertFalse(form.is_valid())