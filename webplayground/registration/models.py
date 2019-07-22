from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    #Let's create a relation with a user model
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profiles',null=True,blank=True)
    bio = models.TextField(null=True,blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)
