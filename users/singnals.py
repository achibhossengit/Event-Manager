from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from users.models import CustomUser
User = CustomUser


@receiver(post_save, sender=User)
# default parameer for post_save signals: sender, instance, created, update_fields(its a tuple which contain update related info like- username, password etc), raw, **kwargs(for send custom parameters)
# default parameer for pre_save signals: sender, instance, raw, using(when used multiple database its define which database used here), **kwargs(for send custom parameters)
def assign_default_role(sender,instance, created, **kwargs):
    if created:
        user_group, created = Group.objects.get_or_create(name='Participant')
        instance.groups.add(user_group)
        instance.save()

@receiver(post_save, sender=User)
def user_activation_mail(sender, created, instance, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        login_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}"

        # sending email
        sub = "User Activation Email"
        body = f"Please active your user account first to log in. Click on activation link bellow:\n{login_url}"
        send_mail(
            subject = sub,
            message = body,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [instance.email],
            fail_silently = True
        )
