from django.dispatch import receiver
from django.db.models.signals import post_save
from clients.models import Client
from .models import Cash


@receiver(post_save, sender=Client)
def _create_new_client_wallets(sender, instance=None, created=None, **kw):
    if created is True:
        if not hasattr(instance, "cash"):
            instance.cash = Cash.objects.create(user=instance)
        