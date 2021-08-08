from django.views.generic import DetailView, ListView, View, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, Http404, HttpResponse, get_object_or_404
from django.urls import reverse_lazy
from itertools import chain
from operator import attrgetter
from ratelimit.mixins import RatelimitMixin
from .models import Tweet, Comment, Like, Bookmark, Retweet
from .forms import TweetCreateForm, CommentCreateForm

# Create your views here.
class TweetListView(LoginRequiredMixin, ListView):
    model = Tweet
    context_object_name = 'tweet_list'
    template_name = 'tweets/tweet_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tweet_create_form'] = TweetCreateForm()
        context['likes'] = list(Like.objects.filter(user=self.request.user).values_list('tweet_id', flat=True))
        context['retweets'] = list(Retweet.objects.filter(author=self.request.user).values_list('origin_id', flat=True))
        context['bookmarks'] = list(Bookmark.objects.filter(user=self.request.user).values_list('tweet_id', flat=True))
        return context

    def get_queryset(self):
        q1 = Tweet.objects.all()
        q2 = Retweet.objects.all()
        combined_qset = sorted(
            chain(q1, q2),
            key=attrgetter('creation_date'),
            reverse=True
        )
        return combined_qset


class TweetCreateView(RatelimitMixin, View):
    ratelimit_key = 'user'
    ratelimit_rate = '1/5s'
    ratelimit_block = True
    ratelimit_method = 'POST'

    def post(self, request):
        form = TweetCreateForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = Tweet(**form.cleaned_data)
            tweet.author = request.user
            tweet.save()
        return redirect('/')


class TweetDetailView(LoginRequiredMixin, DetailView):
    model = Tweet
    context_object_name = 'tweet'
    template_name = 'tweets/tweet_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liked'] = Like.objects.filter(user=self.request.user, tweet=kwargs['object']).first()
        context['retweets'] = list(Retweet.objects.filter(author=self.request.user).values_list('origin_id', flat=True))
        context['comment_create_form'] = CommentCreateForm()
        context['bookmarks'] = list(Bookmark.objects.filter(user=self.request.user).values_list('tweet_id', flat=True))
        return context


class TweetCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        tweet = Tweet.objects.filter(pk=pk).first()
        if tweet is None:
            return Http404
        comment = Comment(origin=tweet, author=request.user, content=request.POST['content'])
        comment.save()
        return redirect(reverse_lazy('tweet_detail', args=[pk]))


class TweetLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        obj = Like.objects.get_or_create(tweet_id=pk, user=request.user)
        like, created = obj
        tweet = like.tweet
        if not created:
            like.delete()
        tweet.likes_count = tweet.get_likes()
        tweet.save()
        return HttpResponse(tweet.likes_count)

    def get(self):
        return Http404


class TweetRetweetView(LoginRequiredMixin, View):
    def post(self, request, pk):
        obj = Retweet.objects.get_or_create(origin_id=pk, author=request.user)
        retweet, created = obj
        if not created:
            retweet.delete()
        return redirect(reverse_lazy('tweet_list'))


class TweetEditView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = Tweet
    context_object_name = 'tweet'
    template_name = 'tweets/tweet_edit.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def post(self, request, pk):
        data = request.POST
        if 'tweet_id' not in data:
            return HttpResponse(status=400)

        tweet = get_object_or_404(Tweet, pk=pk)
        if tweet.author != request.user:
            return HttpResponse(status=403)
        edited = False

        try:
            img = request.FILES['image']
        except Exception:
            img = None

        if 'remove_image' in data and data['remove_image'] == 'on' or img is not None:
            tweet.image.delete()
            tweet.image = img
            edited = True
        if tweet.content != data['content']:
            edited = True
        if edited:
            tweet.edited = True
        tweet.save()
        return redirect(reverse_lazy('tweet_list'))


class TweetDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Tweet
    template_name = 'tweets/tweet_delete.html'
    success_url = reverse_lazy('tweet_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class TweetBookmarkView(LoginRequiredMixin, View):
    def post(self, request, pk):
        obj = Bookmark.objects.get_or_create(tweet_id=pk, user=self.request.user)
        bookmark, created = obj
        if not created:
            bookmark.delete()
        return HttpResponse('Bookmarked')


class BookmarkListView(LoginRequiredMixin, ListView):
    model = Bookmark
    context_object_name = 'bookmarks'
    template_name = 'tweets/bookmark_list.html'

    def get_queryset(self):
        queryset = self.request.user.bookmarks.all()
        return queryset


class CommentDeleteView(LoginRequiredMixin, ListView):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.author == request.user:
            comment.delete()
            return redirect(reverse_lazy('tweet_detail', args=[comment.origin.pk]))
        return HttpResponse(status=403)