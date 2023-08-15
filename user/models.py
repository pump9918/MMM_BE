from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractUser, UserManager

from user.managers import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser, PermissionsMixin):

    username = models.CharField(max_length=128)
    email = models.EmailField(db_index=True, unique=True)
    gender = models.CharField(
        choices=(
            ('F', 'female'),
            ('M', 'male')
        ), max_length=1, blank=True)
    birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=128, blank=True)
    address = models.CharField(max_length=255, blank=True)

    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=10, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class EditorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='editor_profile')
    name = models.CharField(max_length=10, blank=False, null=False)
    address = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.user.email

@receiver(post_save, sender=User)
def create_editor_profile(sender, instance, created, **kwargs):
    if created:
        EditorProfile.objects.create(user=instance)