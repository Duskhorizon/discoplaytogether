from django.db import models
from localusers.models import LocalUser, DiscoServer, DiscoChannel, Membership


# Create your models here.

class Game(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/")
    sub_users = models.ForeignKey(LocalUser, null=True, blank=True, on_delete=models.SET_NULL)
    sub_chan = models.ForeignKey(DiscoChannel, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    creator = models.ForeignKey(LocalUser, null=True, on_delete=models.CASCADE, related_name='creator')
    players = models.ManyToManyField(LocalUser, related_name='player', through='Participation')
    server = models.ForeignKey(DiscoServer, null=True, on_delete=models.CASCADE, related_name='disco_server')

    def __str__(self):
        return self.title


class Participation(models.Model):
    player = models.ForeignKey(LocalUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    notify = models.BooleanField()
    # TODO tworzenie eventu przez uzytkownika ;)
