from django import template
import timeago, datetime, pytz
from ..models import Blog
from django.db.models import Count

register = template.Library()
import readtime

@register.simple_tag
def get_most_liked_posts(count=5):
    return Blog.objects.annotate(
               total_comments=Count('likes')
           ).order_by('-total_comments')[:count]

@register.simple_tag
def get_most_commented_posts(count=5):
    return Blog.objects.annotate(
               total_comments=Count('comments')
           ).order_by('-total_comments')[:count]


@register.filter
def read_time(text):
    return str(readtime.of_text(text))
@register.filter
def ago(d):
    current = datetime.datetime.now(tz=pytz.utc)
#     z = pytz.utc(current)
    return timeago.format(d, current)

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v

    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()

@register.inclusion_tag('post/latest.html')
def show_latest_posts(count=5):
    latest_posts = Blog.objects.order_by('-created_at')[:count]
    return {'latest_posts': latest_posts}


from django.utils.safestring import mark_safe
import markdown


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

