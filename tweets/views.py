from django.views.generic import DetailView, ListView, View, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, Http404, HttpResponse, get_object_or_404
from django.urls import reverse_lazy
from .models import Tweet, Comment, Like, Bookmark
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
        context['bookmarks'] = list(Bookmark.objects.filter(user=self.request.user).values_list('tweet_id', flat=True))
        return context


class TweetCreateView(View):
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
        obj = Like.objects.get_or_create(tweet_id=pk, user=self.request.user)
        like, created = obj
        tweet = like.tweet
        if not created:
            like.delete()
        tweet.likes_count = tweet.get_likes()
        tweet.save()
        return HttpResponse(tweet.likes_count)

    def get(self):
        return Http404


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


class TweetTestView(LoginRequiredMixin, TemplateView):
    template_name = 'tweets/tweet_test.html'

    def post(self, request):
        try:
            content = request.POST['content']
        except Exception:
            return HttpResponse(status=406)

        try:
            img = request.FILES['image']
        except Exception:
            img = None

        Tweet.objects.create(author=request.user, content=content, image=img)
        return redirect(reverse_lazy('tweet_list'))


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