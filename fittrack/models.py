from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Workout(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} workout on {self.date}'
    
class Exercise(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class ExerciseSet(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE,default=1)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    LEVEL = [
        ('Beginner','Beginner'),
        ('Intermediate','Intermediate'),
        ('Advanced','Advanced')
    ]
    intensity = models.CharField(max_length=50,choices=LEVEL,default=1)
    def __str__(self):
        return f"Set for {self.exercise.name} - {self.sets} sets x {self.reps} reps"


# Model for portien Calculator
class ProteinCal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)  

    ACTIVITY_CHOICES = [
        ('Sedentary', 'Sedentary: little or no exercise'),
        ('Light', 'Light: exercise 1-3 times/week'),
        ('Moderate', 'Moderate: exercise 4-5 times/week'),
        ('Active', 'Active: daily exercise or intense exercise 3-4 times/week'),
        ('VeryActive', 'Very Active: intense exercise 6-7 times/week'),
        ('ExtraActive', 'Extra Active: very intense exercise daily, or physical job')
    ]
    activity = models.CharField(max_length=15, choices=ACTIVITY_CHOICES, default='Sedentary')


class CalCount(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    age = models.IntegerField()
    weight = models.DecimalField(max_digits=5,decimal_places=2)
    height = models.DecimalField(max_digits=5,decimal_places=2)
    GENDER = [
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other')
    ]
    gender = models.CharField(max_length=50,choices=GENDER,default=1)
    ACTIVITY_CHOICES = [
        ('Sedentary', 'Sedentary: little or no exercise'),
        ('Light', 'Light: exercise 1-3 times/week'),
        ('Moderate', 'Moderate: exercise 4-5 times/week'),
        ('Active', 'Active: daily exercise or intense exercise 3-4 times/week'),
        ('VeryActive', 'Very Active: intense exercise 6-7 times/week'),
        ('ExtraActive', 'Extra Active: very intense exercise daily, or physical job')
    ]
    activity = models.CharField(max_length=15, choices=ACTIVITY_CHOICES, default='Sedentary')
    GOAL = [
        ('Maintain Weight','Maintain Weight'),
        ('Weight Gain','Weight Gain'),
        ('Weight Loss','Weight Loss')
    ]
    goal = models.CharField(max_length=15,choices=GOAL, default=1)