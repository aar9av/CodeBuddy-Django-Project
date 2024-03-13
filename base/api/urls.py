from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    # for rooms
    path('rooms/', views.getRooms),
    path('room/<str:pk>', views.getRoom),
    
    # for users
    path('users/', views.getUsers),
    path('user/<str:pk>', views.getUser),
    path('user/<str:pk>/update', views.updateUser),
    path('user/<str:pk>/updatesubmissions', views.updateSubmissions),

    # for problems
    path('problems/', views.getProblems),

    # for topics
    path('topics/', views.getTopics),
]