from django.shortcuts import render, redirect
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
import bcrypt
import hashlib, sys
import base64

def Update(request):
    return render(request,'user/user.html')
# Create your views here.
