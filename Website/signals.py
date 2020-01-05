from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core import serializers

from Website.models import Profile, Summoner, Notification, AccessCode
from Website.functions.general import generate_summoner_verification_code


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):

    if created:
        email_confirmed = False
        key = None

        try:
            key = AccessCode.objects.get(registration_interest__email=instance.email)
        except AccessCode.DoesNotExist:
            print('No Access Code!')
            pass

        if key:
            email_confirmed = True

        Profile.objects.create(
            user=instance,
            third_party_token=generate_summoner_verification_code(),
            email_confirmed=email_confirmed
        )


@receiver(post_save, sender=Summoner)
def update_summoner(sender, instance, created, **kwargs):
    if created and not instance.puuid:
        from Website.tasks import update_summoner
        update_summoner.delay(instance.summoner_id, instance.server)


@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created and instance.user:
        from Website.tasks import send_notification
        send_notification.delay(instance.id)
