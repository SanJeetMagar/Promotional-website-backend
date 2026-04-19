from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_contact_emails(self, contact_id, full_name, email, phone, subject, message):
    """
    Sends admin notification and confirmation to visitor.
    Retries on failure.
    """
    try:
        #Admin email 
        admin_subject = f"New Inquiry: {subject or '(no subject)'}"
        admin_context = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "subject": subject,
            "message": message,
        }
        admin_text = render_to_string("emails/contact_admin.txt", admin_context)
        admin_html = render_to_string("emails/contact_admin.html", admin_context)

        admin = EmailMultiAlternatives(
            subject=admin_subject,
            body=admin_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_ADMIN_EMAIL],
        )
        admin.attach_alternative(admin_html, "text/html")
        admin.send(fail_silently=False)
        logger.info(f"Admin email sent for contact {contact_id}")

    #     #Visitor confirmatiom
    #     user_subject = f"Thanks for contacting {settings.SITE_NAME or 'Him Chhaya College'}"
    #     user_context = {"full_name": full_name, "subject": subject, "message": message}
    #     user_text = render_to_string("emails/contact_user.txt", user_context)
    #     user_html = render_to_string("emails/contact_user.html", user_context)

    #     user_msg = EmailMultiAlternatives(
    #         subject=user_subject,
    #         body=user_text,
    #         from_email=settings.DEFAULT_FROM_EMAIL,
    #         to=[email],
    #     )
    #     user_msg.attach_alternative(user_html, "text/html")
    #     user_msg.send(fail_silently=False)
    #     logger.info(f"Confirmation email sent to {email} for contact {contact_id}")

    #     return {"status": "ok"}

    except Exception as exc:
        logger.exception("Failed to send contact emails")
        raise self.retry(exc=exc)
