from django.dispatch import receiver
from django.core.signals import post_save
from .models import Blog

@receiver(post_save, sender=Blog)
def news_letter(sender, instance, **kwargs):
    pass
