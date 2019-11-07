from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from Website.models import Profile, Summoner


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Summoner)
def update_summoner(sender, instance, created, **kwargs):
    if created and not instance.puuid:
        from Website.tasks import update_summoner
        update_summoner.delay(instance.summoner_id, instance.server)
