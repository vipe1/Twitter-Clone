from django import forms
from .models import Tweet, Comment

class TweetCreateForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Type your tweet here',
                'maxlength': 500,
            }),
        }

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'comment-input',
                'placeholder': 'Comment (Press Enter to submit)',
                'maxlength': 100,
            })
        }