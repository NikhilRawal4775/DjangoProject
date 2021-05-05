from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Account(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,null=True)
    email=models.CharField(max_length=100,null=True)
    phone=models.CharField(max_length=13,null=True)
    gender=models.CharField(max_length=1, choices=GENDER_CHOICES,null=True)
    dob=models.DateField(default=timezone.now,null=True)
    address=models.CharField(max_length=100,null=True)
    user_image=models.ImageField(upload_to='img/%y',default='no-user.jpg',null=True,blank=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    name=models.CharField(max_length=200,null=True)
    question=models.TextField(null=True)
    view_response=models.BooleanField(default=True)
    user_response=models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TSurvey(models.Model):
    ques=models.ForeignKey(Question,on_delete=models.CASCADE)
    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    res=models.TextField(null=False,blank=False)

class PQuestion(models.Model):
    name=models.CharField(max_length=200,null=True)
    question=models.TextField(null=True)
    view_response=models.BooleanField(default=True)
    user_response=models.BooleanField(default=True)

    def __str__(self):
        return self.name

class POptions(models.Model):
    ques=models.ForeignKey(PQuestion,on_delete=models.CASCADE,default=None)
    option=models.CharField(max_length=500,null=True,blank=True)
    option_count=models.IntegerField(default=0,null=True)

class MyGallery(models.Model):
    myimage=models.ImageField(upload_to='img/%y',null=True,blank=True,default='dd.png')
    heading=models.CharField(max_length=500,null=True,blank=True)
    body=models.TextField(null=True,blank=True)
    date=models.DateField(default=timezone.now)

    class Meta:
        ordering=['-date']
        

    def __str__(self):
        return self.heading

class Dynamic(models.Model):
    form_name=models.CharField(max_length=500,null=True,blank=True)
    view_response=models.BooleanField(default=True)
    user_response=models.BooleanField(default=True)

    def __str__(self):
        return self.form_name

class DynamicQuestion(models.Model):
    FIELD_CHOICES = (
        ('T', 'text'),
        ('S','select'),
        ('R', 'radio'),
    )
    form=models.ForeignKey(Dynamic,on_delete=models.CASCADE,default=None)
    field_type=models.CharField(max_length=1,default='T', choices= FIELD_CHOICES,null=True)
    ques=models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.ques

class DynamicResponses(models.Model):
    form=models.ForeignKey(DynamicQuestion,on_delete=models.CASCADE,default=None)
    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE,default=None)
    res=models.CharField(max_length=500,null=True,blank=True)

class DynamicOptions(models.Model):
    form=models.ForeignKey(DynamicQuestion,on_delete=models.CASCADE,default=None)
    option=models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.option




