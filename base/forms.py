from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm
from .models import Room, User
#user registration form
from django.contrib.auth.forms import UserCreationForm

#new userregistration form

class newuserRegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' #create a form based on the 'Room' modal fields data
        #exclude (users) and (participants)
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields= ['avatar', 'name','username', 'email', 'bio']

class passresetForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']