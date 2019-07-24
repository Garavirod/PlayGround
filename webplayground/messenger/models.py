from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)#User who creates it
    conent = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
"""
    The thread is a place like a point (punto de encuentro)
    where the thread stores the users and the messages which 
    will be written by the useres

"""
class Thread(models.Model):
    users = models.ManyToManyField(User,related_name='threads') #user.threads all thread the user belong
    messages = models.ManyToManyField(Message)