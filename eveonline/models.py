from django.db import models
from django.contrib.auth.models import User


class EveCharacter(models.Model):
    character_id = models.CharField(max_length=254)
    character_name = models.CharField(max_length=254)
    corporation_id = models.CharField(max_length=254)
    corporation_name = models.CharField(max_length=254)
    corporation_ticker = models.CharField(max_length=254)
    alliance_id = models.CharField(max_length=254)
    alliance_name = models.CharField(max_length=254)
    api_id = models.CharField(max_length=254)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.character_name


class EveApiKeyPair(models.Model):
    api_id = models.CharField(max_length=254)
    api_key = models.CharField(max_length=254)
    user = models.ForeignKey(User)
    error_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username + " - ApiKeyPair"


class EveAllianceInfo(models.Model):
    alliance_id = models.CharField(max_length=254)
    alliance_name = models.CharField(max_length=254)
    alliance_ticker = models.CharField(max_length=254)
    executor_corp_id = models.CharField(max_length=254)
    is_blue = models.BooleanField(default=False)
    member_count = models.IntegerField()

    def __str__(self):
        return self.alliance_name


class EveCorporationInfo(models.Model):
    corporation_id = models.CharField(max_length=254)
    corporation_name = models.CharField(max_length=254)
    corporation_ticker = models.CharField(max_length=254)
    member_count = models.IntegerField()
    is_blue = models.BooleanField(default=False)
    alliance = models.ForeignKey(EveAllianceInfo, blank=True, null=True)

    def __str__(self):
        return self.corporation_name
