from django import template
from tweets.models import Retweet

register = template.Library()

@register.filter()
def is_retweet(obj):
    return isinstance(obj, Retweet)