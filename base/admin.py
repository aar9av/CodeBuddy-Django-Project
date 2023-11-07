from django.contrib import admin

# Register your models here.
from .models import Room, Topic, Message, User # User model is registered by default
from .models import Submission, Problem
admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Submission)
admin.site.register(Problem)