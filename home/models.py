from django.db import models
from django.urls import reverse
# from django_markdown.models import MarkdownField
from taggit.managers import TaggableManager
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD
from django.core.validators import FileExtensionValidator
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.timezone import now


# Create your models here.
class Blog(models.Model):
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200)
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField(default=now)
    text = text = MarkdownField(rendered_field='text_rendered', validator=VALIDATOR_STANDARD)
    text_rendered = RenderedMarkdownField()
    image = models.ImageField(upload_to='image', blank=True)
    tags = TaggableManager()
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('detail', args=(self.pk, self.slug))

class Comment(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField(default=now)
    content = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    class Meta:
        ordering = ['-date']
    def __str__(self):
        return self.name

class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')

class Subscription(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    def __str__(self):
        return self.name
