from django.db import models
from django.contrib.auth.models import User
from optimer.models import optimer
from eveonline.models import EveCharacter
from datetime import datetime
from datetime import date
from django.utils import timezone

def get_sentinel_user():
    return User.objects.get_or_create(username='deleted')[0]

class Paplink(models.Model):
    papdatetime = models.DateTimeField(default=timezone.now())
    duration = models.PositiveIntegerField()
    fleet = models.CharField(max_length=254, default="")
    name = models.CharField(max_length=254)
    hash = models.CharField(max_length=254, unique=True)
    creator = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))

    def __str__(self):
        return self.name


class Pap(models.Model):
    character = models.ForeignKey(EveCharacter)
    paplink = models.ForeignKey(Paplink)
    system = models.CharField(max_length=30)
    shiptype = models.CharField(max_length=30)
    station = models.CharField(max_length=125)
    user = models.ForeignKey(User)

    class Meta:
        unique_together = (('character', 'paplink'),)

    def __str__(self):
        output = "Pap for %s" % self.character.character_name
        return output.encode('utf-8')


class VipPap(models.Model):
    character = models.ForeignKey(EveCharacter)
    paplink = models.ForeignKey(Paplink)
    # user?

    class Meta:
        unique_together = (('character', 'paplink'),)

    def __str__(self):
        output = "VIP pap for %s" % self.character.character_name
        return output.encode('utf-8')