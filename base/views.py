from msilib import Table
from msilib.schema import tables
from multiprocessing import context
from pyexpat import model
from unicodedata import name
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse

#loginrequired decorator
from django.contrib.auth.decorators import login_required
#filter with multiple fields
from django.db.models import Q
#import all models
from .models import Room, Topic, Message, User
#import forms file
from .forms import RoomForm, UserForm, newuserRegForm
#flash messages
from django.contrib import messages
#authentication method
from django.contrib.auth import authenticate, login, logout


# Create your views here.

# LOGIN PAGE VIEW

def loginPage(request):
    #name this page
    page = 'login'
    # restrict user from going to login page if they're logged in
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        #check if  user exists using (try & catch)
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does\'nt exist! ')
        #check if the email & password match
        user = authenticate(email=email, password=password)
        # login user if a match is found
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, "Username & password does\'nt match!")
    content = {'page':page}
    return render(request, 'base/login_register.html', content)

#logout function 

def logoutUser(request):
    logout(request)
    return redirect('home')
#user registration
def userRegister(request):
    #name the page
    page = 'register'
    form = newuserRegForm()
    if request.method == 'POST':
        form = newuserRegForm(request.POST)
        if form.is_valid():
            #login the user rightaway after form is valid
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user) #automatical log the user in after registration
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong during registration, please try again.')
    return render(request, 'base/login_register.html', {'regform':form})

#HOME TEMPLATE VIEW
def home(request):
                                #return all content if there is no filter
    q = request.GET.get('q') if request.GET.get('q') != None else '' 
    #filter 
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))

    topics = Topic.objects.all()[0:5]
    # count number of rooms
    count_room = rooms.count()
    #get comments into activity feeds by filter
    comments = Message.objects.filter(Q(room__topic__name__icontains=q))
    allrooms = {'roomlist': rooms, 'topics':topics, 'count_room': count_room, 'comments':comments}
    return render(request, 'base/home.html', allrooms)

# get each room's details
def room(request , pk):
    room = Room.objects.get(id=pk) 
    #get the number of room's participants
    participants = room.participants.all()
    #comments = room.message_set.all().order_by('-created')
    comments = Message.objects.filter(room=pk).order_by('-created')  #get comments
    comments_no = comments.count() #count number of comments
    #create comments

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        #add the participant to the participants list after writing a comment
        room.participants.add(request.user)
        return redirect('rooms', pk=room.id)
   

    context = {'room': room, 'comments':comments, 'noofcomm':comments_no, 'participants':participants}
  
    return render(request, 'base/rooms.html', context)


#PROFILE TEMPLATE
def userProfile(request, pk):
    # get user's profile name
    user = User.objects.get(id=pk)
    #all rooms for this user
    roomlist = user.room_set.all()
    #user's comments/messages
    comments = user.message_set.all()
    #user's topics
    topics = Topic.objects.all()
    context = {'userlist':user, 'roomlist':roomlist, 'comments':comments, 'topics':topics}

    return render(request, 'base/profile.html', context)

# only access the createroom form if you're logged in , if not you're directed to the login page first
@login_required(login_url='login')
# FORM TEMPLATE
def createRoom(request):
    form = RoomForm()

    topics = Topic.objects.all()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        #create custom topic
        topic_name = request.POST.get('topic')
        topic, created =  Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
  
        return redirect('home')

    context = {'forminfo': form, 'topics':topics}
    return render(request, 'base/roomform.html' , context)


# only access the updateroom form if you're logged in , if not you're directed to the login page first
@login_required(login_url='login')
#UPDATE ROOM
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    
    form = RoomForm(instance=room) #get form values of the room selected
    
    #restrict users from updating other user's info

    if request.user != room.host:
        return HttpResponse('You\'re not allowed to edit this room! ')


    context = {'forminfo':form, 'topics':topics, 'room':room}
    if request.method == 'POST':
        
        topic_name = request.POST.get('topic')
        topic, created =  Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    return render(request, 'base/roomform.html', context)

# only access the delete function if you're logged in , if not you're directed to the login page first
@login_required(login_url='login')
# DELETE ROOM
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk) #get the actual object

    #restrict users from deleting other user's info
    if request.user != room.host:
        return HttpResponse('You\'re not allowed to delete this room! ')

    if request.method == 'POST':
        room.delete() #delete the item
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room} )


# only access the delete function if you're logged in , if not you're directed to the login page first
@login_required(login_url='login')
# DELETE COMMENT
def deleteComment(request, pk):
    message = Message.objects.get(id=pk) #get the actual object

    #restrict users from deleting other user's info
    if request.user != message.user:
        return HttpResponse('You\'re not allowed to delete this room! ')

    if request.method == 'POST':
        message.delete() #delete the item
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message} )
#user profile update

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    formm = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    return render(request, 'base/updateuser.html', {'formm':formm})


#all topics template

def allTopics(request):
    topics = Topic.objects.filter()
    return render(request, 'base/alltopics.html', {'topics':topics})
