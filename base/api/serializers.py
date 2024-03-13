# classes that take a python object to convert into json object
from rest_framework.serializers import ModelSerializer
from base.models import Room, User, Problem, Topic, Submission

class RooomSerializer(ModelSerializer): 
    class Meta: 
        model = Room
        fields = '__all__'

class UserSerializer(ModelSerializer): 
    class Meta: 
        model = User
        fields = '__all__'

class ProblemSerializer(ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class SubmissionSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'