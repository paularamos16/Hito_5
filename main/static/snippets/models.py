from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Flan(models.Model):
    FLAN_TYPE_CHOICES = (
        ('free', 'Free'),
        ('premium', 'Premium'),
        ('diamond', 'Diamond'),
    )
    flan_uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(
        max_length=64
    )
    description = models.TextField()
    image_url = models.URLField()
    slug = models.SlugField()
    is_private = models.BooleanField(default=0)
    type_flan = models.CharField(max_length=10, choices=FLAN_TYPE_CHOICES, default='free')
    
    def __str__(self):
        name = self.name
        type_flan = self.type_flan
        return f'{name} - {type_flan}'

class Contact(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    mensaje = models.CharField(max_length=500)
    
    def __str__(self):
        name = self.nombre
        message = self.mensaje
        return f'{name} : {message}'

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('free', 'Free'),
        ('premium', 'Premium'),
        ('diamond', 'Diamond'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        UserProfile.objects.create(user=instance, user_type='diamond')