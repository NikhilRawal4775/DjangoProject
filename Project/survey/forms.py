from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Account,TSurvey,Question,PQuestion,POptions,Dynamic,DynamicQuestion,MyGallery,DynamicOptions

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter Here'}),
            'email': forms.TextInput(attrs={'placeholder': 'example@gmail.com','type':'email'}),
            'password1': forms.TextInput(attrs={'placeholder': 'Enter Here'}),
            'password2': forms.TextInput(attrs={'placeholder': 'Enter Here'}),
        }

class MyAccount(forms.ModelForm):
    class Meta:
        model=Account
        fields='__all__'
        exclude=['user']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Here'}),
            'dob': forms.TextInput(attrs={'type':'date'}),
            'phone': forms.TextInput(attrs={'placeholder': 'xxxx-xxxxxx','type':'number'}),
            'email': forms.TextInput(attrs={'placeholder': 'xxxxx@xyz.com','type':'email'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter Here'}),
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model=TSurvey
        fields=['res']
        widgets = {
            'res': forms.TextInput(attrs={'placeholder': 'Type What you think :)','type':'text'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model=Question
        fields='__all__'

class PollForm(forms.ModelForm):
    class Meta:
        model=PQuestion
        fields='__all__'


class PollOptionForm(forms.ModelForm):
    class Meta:
        model=POptions
        fields='__all__'

class DynamicForm(forms.ModelForm):
    class Meta:
        model=Dynamic
        fields='__all__'

class DynamicQuestionForm(forms.ModelForm):
    class Meta:
        model=DynamicQuestion
        fields='__all__'

class GalleryForm(forms.ModelForm):
    class Meta:
        model=MyGallery
        fields='__all__'

class DynamicOptionForm(forms.ModelForm):
    class Meta:
        model=DynamicOptions
        fields='__all__'



        
