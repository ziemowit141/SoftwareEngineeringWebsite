from django.db import models
from django.contrib.auth.models import User

class Thesis(models.Model):
    subject = models.CharField(max_length=100, default="None")
    def __str__(self):
        return str(self.subject)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_reviewer = models.BooleanField(default=False)
    academic_degree = models.CharField(max_length=100, default="None")
    picture = models.FileField(default='')
    thesisList = models.ManyToManyField(Thesis)
    def __str__(user):
        return str(user.user)
