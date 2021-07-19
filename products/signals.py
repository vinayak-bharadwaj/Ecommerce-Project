from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        newcart = Order.objects.create(user = instance)


