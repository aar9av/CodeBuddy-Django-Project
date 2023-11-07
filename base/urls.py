from django.urls import path
from . import views

urlpatterns = [
    # why the third parameter name= ' some thing ' is required. 
    # suppose you want to change the url in the future, You don't want to do the redundant task of changing it everywhere.
    # this is how you gonna write the href tag <h5>{{room.id}}. <a href="{% url 'room' room.id %}"> {{room.name}} </a></h5>

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('', views.home, name='home'), 
    path('room/<str:pk>', views.room, name='room'), # in place of <str:pk> it could be <int:pk> or <slug:pk>, pk stands for primary key
    path('profile/<str:username>/', views.userProfile, name='user-profile'),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),

    path('updateUser/', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
]