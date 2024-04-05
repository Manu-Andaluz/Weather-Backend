from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class UserProfile(AbstractBaseUser):
    user = models.OneToOneField(
        User,
        verbose_name=_("user"),
        on_delete=models.CASCADE
        
    )
    secret = models.OneToOneField("master.Secrets",null=True,on_delete=models.CASCADE, related_name="secret")
    is_active = models.BooleanField(default=True)
    onboarding = models.BooleanField(default=True)
