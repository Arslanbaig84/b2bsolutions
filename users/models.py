from django.db import models
from .manager import CustomUserManager
from base.models import BaseModel
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.urls import reverse
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
import datetime

# Create your models here.
class CustomUser(BaseModel, AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True
    )

    def __str__(self) -> str:
        return f'{self.email}'

INDUSTRIES = [
    ('aerospace', 'Aerospace'),
    ('agriculture', 'Agriculture'),
    ('apparel/textile', 'Apparel/Textile'),
    ('automotive', 'Automotive'),
    ('banking', 'Banking'),
    ('chemical_manufacturing', 'Chemical_Manufacturing'),
    ('construction/contrating', 'Construction/Contrating'),
    ('consulting', 'Consulting'),
    ('consumer_goods', 'Consumer_Goods'),
    ('defence', 'Defence'),
    ('e_commerce', 'E_Commerce'),
    ('education', 'Education'),
    ('energy/oil_gas', 'Energy/Oil_Gas'),
    ('engineering', 'Engineering'),
    ('entertainment', 'Entertainment'),
    ('event_management', 'Event_Management'),
    ('food_beverages', 'Food_Beverages'),
    ('govt/utilties', 'Govt/Utilities'),
    ('healthcare/pharma', 'Healthcare/Pharma'),
    ('heavy_equipment', 'Heavy_Equipment'),
    ('it/software/ai', 'IT/Software/AI'),
    ('journalism', 'Journalism'),
    ('legal_services', 'Legal_Services'),
    ('logistic', 'Logistic'),
    ('mining', 'Mining'),
    ('real_estate', 'Real_Estate'),
    ('retail', 'Retail'),
    ('sports', 'Sports'),
    ('telecom', 'Telecom'),
    ('tourism', 'Tourism'),
    ('other', 'Other')
              ]

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    business_name = models.CharField(max_length=200)
    organization_type = models.CharField(max_length=50, choices=[('sole properietor', 'Sole Proprietor'), ('partnership', 'Partnership'), ('private limited', 'Private Limited'), ('public limited', 'Public Limited')])
    business_type = models.CharField(max_length=50, choices=[('trader/wholeseller/distributor', 'Trader/WholeSeller/Distributor'), ('manufacturer', 'Manufacturer'), ('service organization', 'Service Organization')])
    no_of_employees = models.PositiveIntegerField(choices=[('1-10', '1-10'), ('11-25', '11-25'), ('26-50', '26-50'), ('50-100', '50-100'), ('100-500', '100-500'), ('500+', '500+')])
    industry_type = models.CharField(max_length=100, choices=INDUSTRIES)
    ntn_validator = RegexValidator(
        regex=r'^\d{7}-\d{1}$',
        message="NTN must be in the format '1234567-8'"
    )
    ntn = models.CharField(max_length=9, unique=True, validators=[ntn_validator], null=True, blank=True)
    contact = models.CharField(max_length=20, unique=True, null=True, blank=True)
    whatsapp = models.CharField(max_length=20)
    website = models.URLField(null=True, blank=True)
    address1 = models.CharField(max_length=200, null=True, blank=True)
    address2 = models.CharField(max_length=200, null=True, blank=True)
    establishment_year = models.IntegerField(validators=[
        MinValueValidator(1900),
        MaxValueValidator(datetime.date.today().year)
    ])

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)  # Create UserProfile instance


@receiver(post_save, sender=CustomUser)
def send_verification_email(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        # Prepare to send the email
        domain = getattr(settings, 'SITE_DOMAIN', 'http://127.0.0.1:8000/')
        mail_subject = 'Activate your account'
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        token = account_activation_token.make_token(instance)
        verification_url = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        
        message = render_to_string('users/account_verification_email.html', {
            'user': instance,
            'domain': domain,
            'uid': uid,
            'token': token,
            'verification_url': verification_url
        })
        to_email = instance.email

        # Send the email
        email = EmailMultiAlternatives(
            subject=mail_subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email]
        )
        email.attach_alternative(message, "text/html")
        email.send()
