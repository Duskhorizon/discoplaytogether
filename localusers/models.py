from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class DiscoChannel(models.Model):
    name = models.CharField(max_length=30)
    uid = models.TextField(default="0")

    def __str__(self):
        return self.name


class DiscoServer(models.Model):
    name = models.CharField(max_length=30)
    uid = models.TextField(default="0")
    channels = models.ForeignKey(DiscoChannel, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class LocalUser(AbstractUser):
    verified = models.BooleanField(default=False)
    servers = models.ManyToManyField(DiscoServer, through='Membership', related_name='servers')


class Membership(models.Model):
    user = models.ForeignKey(LocalUser, on_delete=models.CASCADE)
    server = models.ForeignKey(DiscoServer, on_delete=models.CASCADE)
    admin = models.BooleanField(default=False)
    subbed = models.BooleanField(default=False)
