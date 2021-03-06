from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from account.models import Company
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver

from alababak import settings


class User(AbstractUser):
    type = models.CharField(max_length=30, null=True, default='admin')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
