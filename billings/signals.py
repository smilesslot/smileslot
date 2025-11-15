from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from saas.models import get_broker


@receiver(post_save, sender=get_user_model())
def on_user_post_save(sender, instance, created, raw, **kwargs):
    #pylint:disable=unused-argument
    if created and instance.is_superuser:
        get_broker().add_manager(instance)
