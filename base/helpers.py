from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

# Function to send email verification
def verification_email(user):
    # Generate token and encoded user ID
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Build the activation link
    activation_link = f"http://your-domain.com{reverse('account_activation', kwargs={'uidb64': uid, 'token': token})}"
    
    # Prepare the email content using an HTML template
    subject = "Verify Your Email Address"
    message = render_to_string('email_verification_template.html', {
        'user': user,
        'activation_link': activation_link,
    })

    # Send the email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
