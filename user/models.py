from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractUser, UserManager

from user.managers import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

class Address(models.Model):
    province = models.CharField(
        choices=(
        ('Seoul', '서울특별시'),
        ('Gyeonggi', '경기도'),
        ('Incheon', '인천광역시'),
        ('Gangwon', '강원도'),
        ('Chungbuk', '충청북도'),
        ('Chungnam', '충청남도'),
        ('Gyeongbuk', '경상북도'),
        ('Gyeongnam', '경상남도'),
        ('Jeju', '제주특별자치도'),
        ('Jeonbuk', '전라북도'),
        ('Jeonnam', '전라남도'),
        ), max_length=50, blank=False, null=False)
    
    city = models.CharField(
        choices=(
        ('Jungguo', '중구'),
        ('Jongrogu', '종로구'),
        ('Yongsangu', '용산구'),
        ('Seongdonggu', '성동구'),
        ('Gwangjingu', '광진구'),
        ('Dongdaemungu', '동대문구'),
        ('Jungranggu', '중랑구'),
        ('Seongbukgu', '성북구'),
        ('Gangbukgu', '강북구'),
        ('Dobonggu', '도봉구'),
        ('Nowongu', '노원구'),
        ('Eunpyeonggu', '은평구'),
        ('Seodaemungu', '서대문구'),
        ('Mapogu', '마포구'),
        ('Yangcheongu', '양천구'),
        ('Gangseogu', '강서구'),
        ('Gurogu', '구로구'),
        ('Geumcheongu', '금천구'),
        ('Uijeongbu', '의정부시'),
        ('Goyang', '고양시'),
        ('Yangju', '양주시'),
        ('Dongducheon', '동두천시'),
        ('Guri', '구리시'),
        ('Namyangju', '남양주시'),
        ('Paju', '파주시'),
            
            
        ), max_length=50, blank=True, null=True)
    
class User(AbstractUser, PermissionsMixin):
    user_ID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=128)
    email = models.EmailField(db_index=True, unique=True)
    gender = models.CharField(
        choices=(
            ('F', 'female'),
            ('M', 'male')
        ), max_length=1, blank=True)
    birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=128, blank=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='user_address', blank=True, null=True)


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
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='profile_address', blank=True, null=True)


    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class EditorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='editor_profile')
    name = models.CharField(max_length=10, blank=False, null=False)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='editor_address', blank=True, null=True)
    email = models.EmailField(db_index=True, unique=True, null=False, blank=False)

    def __str__(self):
        return self.user.email

@receiver(post_save, sender=User)
def create_editor_profile(sender, instance, created, **kwargs):
    if created:
        EditorProfile.objects.create(user=instance)
        
        
