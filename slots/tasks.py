from django.core.mail import EmailMessage
from django.utils.translation import gettext as _

from appointment.email_sender import notify_admin, send_email
from appointment.logger_config import get_logger
from appointment.models import Appointment

logger = get_logger(__name__)


def send_email_reminder(to_email, first_name, reschedule_link, appointment_id):
    """
    Send a reminder email to the client about the upcoming appointment.
    """

    # Fetch the appointment using appointment_id
    logger.info(f"Sending reminder to {to_email} for appointment {appointment_id}")
    appointment = Appointment.objects.get(id=appointment_id)
    recipient_type = 'client'
    email_context = {
        'first_name': first_name,
        'appointment': appointment,
        'reschedule_link': reschedule_link,
        'recipient_type': recipient_type,
    }
    send_email(
            recipient_list=[to_email], subject=_("Reminder: Upcoming Appointment"),
            template_url='email_sender/reminder_email.html', context=email_context
    )
    # Notify the admin
    logger.info(f"Sending admin reminder also")
    email_context['recipient_type'] = 'admin'
    notify_admin(
            subject=_("Admin Reminder: Upcoming Appointment"),
            template_url='email_sender/reminder_email.html', context=email_context
    )


def send_email_task(recipient_list, subject, message, html_message, from_email, attachments=None):
    try:
        email = EmailMessage(
                subject=subject,
                body=message if not html_message else html_message,
                from_email=from_email,
                to=recipient_list
        )

        if html_message:
            email.content_subtype = "html"

        if attachments:
            for attachment in attachments:
                email.attach(*attachment)

        email.send(fail_silently=False)
    except Exception as e:
        logger.error(f"Error sending email from task: {e}")


def notify_admin_task(subject, message, html_message):
    """
    Task function to send an admin email asynchronously.
    """
    try:
        from django.core.mail import mail_admins
        logger.info(f"Sending admin email with subject: {subject}")
        mail_admins(subject=subject, message=message, html_message=html_message, fail_silently=False)
    except Exception as e:
        logger.error(f"Error sending admin email from task: {e}")
