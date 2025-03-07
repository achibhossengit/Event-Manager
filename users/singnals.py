from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail

@receiver(post_save, sender=User)
# default parameer for post_save signals: sender, instance, created, update_fields(its a tuple which contain update related info like- username, password etc), raw, **kwargs(for send custom parameters)
# default parameer for pre_save signals: sender, instance, raw, using(when used multiple database its define which database used here), **kwargs(for send custom parameters)
def assign_default_role(sender,instance, created, **kwargs):
    if created:
        user_group, created = Group.objects.get_or_create(name='Participant')
        instance.groups.add(user_group)
        instance.save()

# @receiver(post_save, sender=User)
# def activate_user_email(sender, instance, created, **kwargs):
#     if created:
#         # print(vars(instance))
#         user_email = instance.email
        
#         send_mail(
#         "Subject here",
#         "Here is the message.",
#         "from@example.com",
#         ["to@example.com"],
#         fail_silently=False,
#         )
