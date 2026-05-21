from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger('core')


def send_absence_notification(student, date):
    """
    Send email notification when a student is marked absent.
    Only sends if the student has an email address.
    """
    if not student.email:
        logger.info(f"No email for student {student.name} - skipping notification")
        return False

    subject = f"Absence Notification - {student.name}"

    message = f"""
Dear Parent/Guardian,

This is to inform you that {student.name} (Admission No: {student.admission_number}) 
was marked ABSENT on {date.strftime('%B %d, %Y')}.

Class: {student.class_level}

If this is an error or you have already informed the school, please disregard this message.

For any queries, please contact the school administration.

Regards,
Eldoret National Poly ICT Group B
School Management System
    """.strip()

    html_message = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: #1a237e; padding: 20px; text-align: center;">
            <h2 style="color: white; margin: 0;">Eldoret National Poly ICT Group B</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0;">Absence Notification</p>
        </div>

        <div style="padding: 30px; background: #f5f7ff;">
            <div style="background: #ffebee; border-left: 4px solid #c62828; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
                <strong style="color: #c62828;">⚠️ Student Absent</strong>
            </div>

            <p>Dear Parent/Guardian,</p>

            <p>This is to inform you that:</p>

            <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
                <tr style="background: #e8eaf6;">
                    <td style="padding: 10px; font-weight: bold;">Student Name</td>
                    <td style="padding: 10px;">{student.name}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; font-weight: bold;">Admission No.</td>
                    <td style="padding: 10px;">{student.admission_number}</td>
                </tr>
                <tr style="background: #e8eaf6;">
                    <td style="padding: 10px; font-weight: bold;">Class</td>
                    <td style="padding: 10px;">{student.class_level}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; font-weight: bold;">Date Absent</td>
                    <td style="padding: 10px; color: #c62828; font-weight: bold;">{date.strftime('%B %d, %Y')}</td>
                </tr>
            </table>

            <p>If this is an error or you have already informed the school, please disregard this message.</p>

            <p>For any queries, please contact the school administration.</p>

            <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">
            <p style="color: #9e9e9e; font-size: 0.85rem; text-align: center;">
                This is an automated message from the School Management System.
            </p>
        </div>
    </div>
    """

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Absence notification sent to {student.email} for {student.name}")
        return True
    except Exception as e:
        logger.error(f"Failed to send absence notification for {student.name}: {e}")
        return False
