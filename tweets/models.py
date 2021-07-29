from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from PIL import Image

def get_upload_path(instance, filename):
    name = datetime.now().strftime('%Y%m%d%H%M%S')
    ext = filename[filename.rfind('.'):]
    path = f'tweets/author-{instance.author.pk}/{name}{ext}'
    return path

# Create your models here.
class Tweet(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='tweets'
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    content = models.TextField(max_length=500)
    image = models.ImageField(blank=True, null=True, upload_to=get_upload_path)
    likes_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return self.content[:50]

    def get_likes(self):
        count = Like.objects.filter(tweet__id=self.id).count()
        return count


class Comment(models.Model):
    origin = models.ForeignKey(
        Tweet,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='comments'
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return self.content[:50]


class Like(models.Model):
    tweet = models.ForeignKey(
        Tweet,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='likes'
    )

    def __str__(self):
        return f'L: {self.user} - {self.tweet}'


class Bookmark(models.Model):
    tweet = models.ForeignKey(
        Tweet,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )

    def __str__(self):
        return f'B: {self.user} - {self.tweet}'