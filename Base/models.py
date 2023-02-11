from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=True)
    short_description = models.TextField(max_length=100, null=True)


    CHOICES = (
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner')
    )
    dish_type = models.CharField(choices=CHOICES,
                                 default='Breakfast',
                                 null=True,
                                 max_length=10)

    def __str__(self):
        return f'{self.title}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    username = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=50, null=True, unique=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return str(self.user)

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.content[:15]

class Notification(models.Model):
    message = models.CharField(max_length=70)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)