from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm): 
    # create a form that inherits from UserCreationForm
    class Meta: 
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm): 
    class Meta: 
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        # fields = ['avatar', 'first_name', 'last_name', 'username', 'email', 'bio', 'codechef_id', 'leetcode_id', 'codeforces_id']
        fields = ['avatar', 'codechef_id', 'codeforces_id', 'leetcode_id', 'bio']
