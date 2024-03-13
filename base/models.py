from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password=None):
        if not username:
            raise ValueError('Users must have a username')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, password):
        user = self.create_user(
            username,
            first_name,
            last_name,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser): 
    username = models.CharField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    gender = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Male')

    codechef_id = models.CharField(max_length=255, null=True)
    leetcode_id = models.CharField(max_length=255, null=True)
    codeforces_id = models.CharField(max_length=255, null=True)

    codechef_rating = models.IntegerField(null=True, default=0)
    leetcode_rating = models.IntegerField(null=True, default=0)
    codeforces_rating = models.IntegerField(null=True, default=0)

    created_at = models.DateTimeField(default=timezone.now, null=True)
    last_edited_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def leetcode_url(self):
        return f"https://leetcode.com/{self.leetcode_id}"

    @property
    def codeforces_url(self):
        return f"https://codeforces.com/profile/{self.codeforces_id}"

    @property
    def codechef_url(self):
        return f"https://www.codechef.com/users/{self.codechef_id}"

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    @property
    def is_staff(self):
        return self.is_admin

class Problem(models.Model):
    url = models.URLField(primary_key=True)
    title = models.CharField(max_length=255)
    platform = models.CharField(max_length=10, choices=[('Codechef', 'Codechef'), ('Leetcode', 'Leetcode'), ('Codeforces', 'Codeforces')])
    created_at = models.DateTimeField(default=timezone.now)
    last_edited_at = models.DateTimeField(auto_now=True)

class Submission(models.Model):
    submission_id = models.CharField(max_length=255, primary_key=True, default='0')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='submissions')
    submission_link = models.URLField()
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    created_at = models.DateTimeField(default=timezone.now)
    last_edited_at = models.DateTimeField(auto_now=True)

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self): 
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) # if the Topic were defined below all other models, it should be wrapped in single quotes.
    name = models.CharField(max_length=200)
    # setting null = true means it can be blank. null is for the databases, blank is for the form and saving
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True) # current active people
    updated = models.DateTimeField(auto_now=True) # we will be automatically sets to the time when last updated.
    # the only difference from auto_now is that it gets its value only once the first time when the table was created
    created = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ['-updated', '-created'] # - is to set the ordering in descending order, without this, it is automatically set in ascending order

    def __str__(self): 
        return self.name # the only difference from auto_now is that it gets its value only once the first time when the table was created

class Message(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # in place of cascade, you could do SET_NULL to avoid deleting messages when Room is deleted. Cascade means it gets deleted when it is deleted.
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ['-updated', '-created'] # - is to set the ordering in descending order, without this, it is automatically set in ascending order

    def __str__(self):
        return self.body[0:50]
    