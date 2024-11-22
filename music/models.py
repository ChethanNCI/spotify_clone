from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_subscribed = models.BooleanField(default=False)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {'Subscribed' if self.is_subscribed else 'Not Subscribed'}"