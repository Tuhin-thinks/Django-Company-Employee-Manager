from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from companyusers.models import User
from tasks.send_email import email_token_created


@receiver(post_save, sender=User)
def create_user_token(sender, instance, created=False, **kwargs):
    if created:
        token = Token.objects.create(user=instance)

        # store the token in the user model
        instance.token = token.key
        instance.update()

        email_token_created(instance.email, token.key)
