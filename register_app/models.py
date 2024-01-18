import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager


class Clients(models.Model):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CLIENT = "CLIENT", "Client"

    class Plans(models.TextChoices):
        PREMIUM = 'Premium', 'Premium'
        BASIC = 'Basic', 'Basic'

    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=256)
    client_short = models.CharField(max_length=20,null=True)
    role_type = models.CharField(max_length=10, choices=Roles.choices, default=Roles.CLIENT)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_onboarded = models.DateTimeField(auto_now_add=True)
    plans = models.CharField(max_length=40,choices=Plans.choices,default=Plans.BASIC)
    # logos = models.ImageField(upload_to='client_logos/', default="None")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'clients'

    def __str__(self):
        return self.username


class Site_Configs(models.Model):
    class SiteType(models.TextChoices):
        SOLAR = 'Solar', 'Solar'
        WIND = 'Wind', 'Wind'

    class Plans(models.TextChoices):
        PREMIUM = 'Premium', 'Premium'
        BASIC = 'Basic', 'Basic'

    site_id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, editable=False)

    site_name = models.CharField(max_length=20)
    state = models.CharField(max_length=40)
    capacity = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=12, choices=SiteType.choices, default=SiteType.SOLAR)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    log_ts = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    client_name = models.ForeignKey(Clients, on_delete=models.CASCADE, to_field='username', related_name='client_name')
    variables = models.CharField(max_length=256)  ## Get all the variables list here
    ac_dc = models.FloatField(blank=True,null=True)

    def __str__(self):
        return self.site_name


class SiteVerification(models.Model):
    # id = models.BigIntegerField(unique=True, primary_key=True)
    site_v_id = models.ForeignKey(Site_Configs, on_delete=models.CASCADE, to_field='site_id', related_name='site_v_id')
    site_status = models.BooleanField(choices=(("ACTIVE", True), ("INACTIVE", False)), default=False)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.site_v_id
