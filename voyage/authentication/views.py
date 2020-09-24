from django.shortcuts import render, redirect
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

def Home(request):
    return render(request,'authentication/home.html')




# Create your views here.
