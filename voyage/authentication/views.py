from django.shortcuts import render, redirect
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

def Home(request):
    return render(request,'authentication/home.html')

def Log_In(request):
    return render(request,'authentication/login.html')

def Sign_Up(request):
    return render(request,'authentication/signup.html')


# Create your views here.
