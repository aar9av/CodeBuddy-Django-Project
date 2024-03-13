# JSON - Javascript Object Notation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room, User, Problem, Topic, Submission
from django.core.exceptions import ObjectDoesNotExist
from .serializers import RooomSerializer, UserSerializer, ProblemSerializer, TopicSerializer, SubmissionSerializer

@api_view(['GET'])
def getRoutes(request): 
    routes = [
        'GET /api',
        # for rooms
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)

# for rooms
# ---------------------------------------------------
@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RooomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RooomSerializer(room, many=False)
    return Response(serializer.data)

# ---------------------------------------------------

# for users
# ---------------------------------------------------
@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
def updateUser(request, pk):
    data = request.data
    user = User.objects.get(username=pk)
    if 'email' in data:
        user.email = data['email']
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'bio' in data:
        user.bio = data['bio']
    if 'gender' in data:
        user.gender = data
    if 'codechef_id' in data:
        user.codechef_id = data['codechef_id']
    if 'leetcode_id' in data:
        user.leetcode_id = data['leetcode_id']
    if 'codeforces_id' in data:
        user.codeforces_id = data['codeforces_id']
    if 'codechef_rating' in data:
        user.codechef_rating = data['codechef_rating']
    if 'leetcode_rating' in data:
        user.leetcode_rating = data['leetcode_rating']
    if 'codeforces_rating' in data:
        user.codeforces_rating = data['codeforces_rating']
    if 'avatar' in data:
        user.avatar = data['avatar']

    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def updateSubmissions(request, pk):
    data = request.data
    user = User.objects.get(username=pk)
    retdata = []
    for submission in data:
        try:
            problem = Problem.objects.get(url=submission['problem_link'])
        except ObjectDoesNotExist:
            problem = Problem.objects.create(
                title=submission['problem_title'],
                url=submission['problem_link'],
                platform=submission['platform'],
            )
        try: 
            submission = Submission.objects.get(submission_id=submission['submission_id'])
        except ObjectDoesNotExist:
            submission = Submission.objects.create(
                submission_id=submission['submission_id'],
                problem=problem,
                submission_link=submission['submission_url'],
                submitted_by=user,
            )
    return Response(retdata)
        

@api_view(['GET'])
def getUser(request, pk):
    user = User.objects.get(username=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

# ---------------------------------------------------

# for problems
# ---------------------------------------------------
@api_view(['GET'])
def getProblems(request):
    problems = Problem.objects.all()
    serializer = ProblemSerializer(problems, many=True)
    return Response(serializer.data)
# ---------------------------------------------------

# for topics
# ---------------------------------------------------
@api_view(['GET'])
def getTopics(request):
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)
# ---------------------------------------------------