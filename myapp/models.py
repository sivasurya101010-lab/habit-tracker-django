from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class HabitCategory(models.Model):
    name=models.CharField(max_length=20,validators=[MinLengthValidator(3)])
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name
    

class Habit(models.Model):
    title=models.CharField(max_length=100,validators=[MinLengthValidator(3)])
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.ForeignKey(HabitCategory,on_delete=models.CASCADE,null=True,blank=True)
    max_streak=models.IntegerField(default=0)



class HabitLog(models.Model):
    habit=models.ForeignKey(Habit,on_delete=models.CASCADE)
    completion=models.BooleanField(default=False)
    logdate=models.DateField(auto_now_add=True)


class profile(models.Model):

    class Gender(models.TextChoices):
        MALE='M','Male'
        FEMALE='F','Female'

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    gender=models.CharField(max_length=1,choices=Gender.choices,blank=True,null=True)
    ph_no=models.CharField(blank=True,null=True,max_length=10)
    picture=models.ImageField( upload_to='profile_pics/',default='profile_pics/default.jpg')

    def __str__(self):
        return self.user.username


    

