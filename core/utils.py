import uuid, random
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.urls import reverse

def send_verification_email(user, request):
    """Send verification email with both code and link"""

    # Generate both token and code
    token = str(uuid.uuid4())
    code = str(random.randint(100000, 999999))
    user.verification_token = token
    user.verification_code = code
    from django.utils import timezone
    user.verification_sent_at = timezone.now()
    user.save(update_fields=["verification_token", "verification_code", "verification_sent_at"])

    # Build verification URL
    verify_url = request.build_absolute_uri(
        reverse("core:verify_email") + f"?token={token}"
    )

    subject = "Verify Your Account"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [user.email]

    html_content = f"""
    <html>
    <body style="font-family:Arial,sans-serif;">
        <p>Hello <b>{user.first_name or user.username}</b>,</p>
        <p>Thank you for registering!</p>
        <p>Your verification code is:</p>
        <h2 style="text-align:center; color:#0d6efd;">{code}</h2>
        <p>Or verify by clicking the button below:</p>
        <p style="text-align:center;">
            <a href="{verify_url}" 
               style="background:#0d6efd;color:white;padding:10px 20px;
                      text-decoration:none;border-radius:6px;">Verify My Email</a>
        </p>
        <p>If the button doesn’t work, copy this URL:</p>
        <p><a href="{verify_url}">{verify_url}</a></p>
        <br>
        <p>Thanks,<br>The Convention Hall Management Team</p>
    </body>
    </html>
    """

    msg = EmailMultiAlternatives(subject, "", from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
