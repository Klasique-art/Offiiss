from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.core.mail import send_mail

@receiver(post_save, sender=Profile)
def notice(sender, instance, **kwargs):pass
    # if instance.agent_status == 3:
        # send_mail("Offiiss account verification confirmation", f"congratulations {instance.user.first_name}. \rYour agent account is successfully verified importers can now see your profile on the offiiss app. \rThank you.", "offiissapp@offiiss.com", [instance.user.email], fail_silently=True)
