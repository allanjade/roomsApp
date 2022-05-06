from csv import field_size_limit
from email.policy import default
from optparse import Values
from statistics import mode
from time import timezone
from tkinter.tix import Tree
from django.db import models
# from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

#abstract user model
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, error_messages= { 'required':"You must enter your email"})
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default='avatar.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


#================================Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
#======================create a table class
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200) 
    participants = models.ManyToManyField(User, related_name='participants', blank=True) #creats many to many relationship for user
    description = models.TextField(null=True, blank=True)
    email = models.CharField(max_length=255, null=False, default=timezone)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

#=====================order values by (date created/update)
    class Meta:
        ordering = ['-updated', '-created']

 #=====================pass string representation
    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
#=================delete  user's content if room is deleted i.e. using CASCADE
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
   
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
 
                                                #======================order values by (date created/update)
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        
        return self.body[0:50]
        
        
