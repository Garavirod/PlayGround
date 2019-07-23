from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver # Decorator
from django.db.models.signals import post_save
# Create your models here.
class Profile(models.Model):
    #Let's create a relation with a user model
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profiles',null=True,blank=True)
    bio = models.TextField(null=True,blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)

#Signal
@receiver(post_save,sender=User) #User is a model which sends the signal o execute the trigger
def ensure_profile_exists(sender,instance,**kwargs):
    if kwargs.get('created',False ):
        #If exisits 'created' it's the first time that the instance has been created
        Profile.objects.get_or_create(user=instance)
        print("-----Profile created-----")