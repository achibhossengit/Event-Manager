from django.db.models.signals import m2m_changed
from event.models import Event
from users.models import CustomUser
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
User = CustomUser

@receiver(m2m_changed, sender=Event.participants.through)
def confirmation_mail(sender, action, instance, pk_set, **kwargs):
    # without condition it will triggred two times - "pre_add" and "post_add" 
    if action == 'post_add':
        user_id = list(pk_set)[0]
        user = User.objects.get(id=user_id)
        sub = 'Event Confirmation Mail'
        # body = f"Thanks for booked bellow events. \n\nEvent Name: {instance.name} \nDescriptions: {instance.description} \nDate: {instance.date} \nTime: {instance.time} \n\nHope you join this event proper time."
        email_body = render_to_string('event_booked_mail.html', {
            'user': user,
            'event': instance,
        })
        send_mail(
            subject = sub,
            message = '',
            html_message=email_body,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [user.email],
            fail_silently = True
        )