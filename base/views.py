from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User, Submission
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.http import HttpResponse


# Create your views here.

'''
rooms = [
    {'id': 1, 'name': 'Lets Learn Python!'},
    {'id': 2, 'name': 'Design with me'},
    {'id': 3, 'name': 'Frontend Developers'},
]
'''

# don't use login() because there is built in login function and there will be a conflict
def loginPage(request): 
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST': 
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try: 
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, email=email, password=password)
        if user is not None: 
            login(request, user) # this create a session in the browser cookies
            return redirect('home')
        else: 
            messages.error(request, 'Username or Password does not match')
    context = {'page' : page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request): 
    form = MyUserCreationForm()
    if request.method == 'POST': 
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # getting the user data without committing it to the database
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request, 'An error occurred during registration.')

    return render(request, 'base/login_register.html', {'form' : form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # here __ means going to the parent of topic, topic here is the attribute of the table and topic__name is the parent topic's attribute
    rooms = Room.objects.filter( Q( topic__name__icontains=q ) | 
                                 Q(name__icontains=q) |
                                 Q(description__icontains=q) )
    # i means case insensitive and 'contains' double checks if the query exists or not
    # rooms = Room.objects.all() # get all the table rows as objects.

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count() # count function is faster than len function
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context = {'rooms': rooms, 'topics' : topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context) # here the list of rooms is passed in the form of dictionary

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created') # we can query child objects of a specific room here
    participants = room.participants.all()

    if request.method == 'POST': 
        message = Message.objects.create(
            user = request.user, 
            room = room, 
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',  pk=room.id) # because it is post request, but we want to land the page back with get request to avoid any malfunction

    '''
    room = None
    for i in rooms: 
        if i['id'] == int(pk): 
            room = i 
            break
    '''
    context = {'room' : room, 'room_messages' : room_messages, 'participants' : participants}
    return render(request, 'base/room.html', context)


def userProfile(request, username):
    user = User.objects.get(username=username)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user' : user, 'rooms' : rooms, 'room_messages' : room_messages, 'topics' : topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST': 
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name) # if newly one is created, created will be true otherwise it will be false. 
        Room.objects.create(
            host = request.user, 
            topic = topic, 
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')
        # print(request.POST) # prints all the data filled by user
        # print(request.POST.name) # prints only name attribute of the form
        # form = RoomForm(request.POST)
        # if form.is_valid(): 
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
    context = {'form' : form, 'topics' : topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk): 
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host: 
        return HttpResponse('You are not the owner.')

    if request.method == 'POST': 
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name) # if newly one is created, created will be true otherwise it will be false. 
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    
    context = {'form' : form, 'topics' : topics, 'room' : room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk): 
    room = Room.objects.get(id=pk)
    if request.user != room.host: 
        return HttpResponse('You are not the owner.')

    if request.method == 'POST': 
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request, pk): 
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('You are not the owner.')


    if request.method == 'POST': 
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='login')
def updateUser(request): 
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST': 
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid(): 
            form.save()
            return redirect('user-profile', username=user.username)

    return render(request, 'base/update-user.html', {'form' : form})

def topicsPage(request): 
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics' : topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages' : room_messages})

def user_submissions(request, username):
    submissions = Submission.objects.filter(submitted_by_id=username)
    context = {
        'submissions': submissions
    }
    return render(request, 'submissions.html', context)