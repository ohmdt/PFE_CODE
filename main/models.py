from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    goal = models.IntegerField(blank=True, null=True)
    activity_level = models.IntegerField(blank=True, null=True)

    @property
    def get_activity(self):
        if self.activity_level == 1:
            return "No or very little exercise"
        if self.activity_level == 2:
            return "Exercise 1-3 times/week"
        if self.activity_level == 3:
            return "Exercise 4-5 times/week"
        if self.activity_level == 4:
            return "Daily exercise or intense exercise 3-4 times/week"
        if self.activity_level == 5:
            return "Intense exercise 6-7 times/week"

    def __str__(self):
        return self.user.get_full_name()
