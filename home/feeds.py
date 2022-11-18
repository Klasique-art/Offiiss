from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Blog


class LatestPostsFeed(Feed):
    title = 'Sewonet blog'
    link = reverse_lazy('home')
    description = 'New post on Sewonet blog'

    def items(self):
        return Blog.objects.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.text, 30)
