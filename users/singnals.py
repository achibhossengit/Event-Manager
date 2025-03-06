from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=User)
# default parameer for post_save signals: sender, instance, created, update_fields(its a tuple which contain update related info like- username, password etc), raw, **kwargs(for send custom parameters)
# default parameer for pre_save signals: sender, instance, raw, using(when used multiple database its define which database used here), **kwargs(for send custom parameters)
def assign_default_role(sender,instance, created, **kwargs):
    if created:
        user_group, created = Group.objects.get_or_create(name='Participant')
        instance.groups.add(user_group)
        instance.save()