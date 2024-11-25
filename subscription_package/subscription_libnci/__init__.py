from django.contrib.auth.models import User
from django.db import transaction
from music.models import Subscription

def subscribe_user(user):
    """Subscribes a user if they are not already subscribed."""
    # Use get_or_create to avoid duplicate subscriptions
    subscription, created = Subscription.objects.get_or_create(user=user)
    
    if subscription.is_subscribed:
        return False  # Already subscribed, so return False

    with transaction.atomic():
        subscription.is_subscribed = True
        subscription.save()
    return True  # Successfully subscribed


def unsubscribe_user(user):
    """Unsubscribes a user if they are subscribed."""
    subscription = Subscription.objects.filter(user=user, is_subscribed=True).first()
    if subscription:
        subscription.is_subscribed = False
        subscription.save()
        return True
    return False
