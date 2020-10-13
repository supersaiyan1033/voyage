from django.shortcuts import render, redirect
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
from django.contrib import messages
import bcrypt
import hashlib, sys
import base64

def Home(request):
    return render(request,'authentication/home.html')

def Log_In(request):
     if request.method == "POST":
          email = request.POST.get('email')
          password = request.POST.get('password')
          
          cursor = connection.cursor()
          cursor.execute("""SELECT * FROM users WHERE email= %s""",[email])
          row = cursor.fetchall()
          if cursor.rowcount ==1:
             dbpassword = row[0][6]
             print(dbpassword)
             if bcrypt.checkpw(password.encode('utf8'),dbpassword.encode('utf8')):
                 messages.success(request,'Login successful!!')
                 return render (request,'authentication/user.html')
             else:
               messages.success(request,'incorrect password please try again!!')
               return render(request,'authentication/login.html')
          else:
            messages.success(request,'Account does not exist with the entered credentials!! signup to create an account')
            return render(request,'authentication/login.html')
     else:
       return render(request,'authentication/login.html')


def Sign_Up(request):
     if request.method == "POST":
          firstname = request.POST.get('firstname')
          lastname = request.POST.get('lastname')
          gender = request.POST.get('gender')
          address = request.POST.get('address')
          DOB = request.POST.get('DOB')
          mobileno = request.POST.get('mobileno')
          email = request.POST.get('email')
          password = request.POST.get('password')
          password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(rounds=12))

          cursor = connection.cursor()
          cursor.execute("""SELECT * FROM users WHERE email = %s""",[email])
          row = cursor.fetchall()
          if cursor.rowcount==0:
             cursor.execute("""INSERT INTO users (firstname,lastname,gender,address,mobileno,email,password,DOB) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""", (firstname ,lastname,gender,address,mobileno,email,password,DOB))
             return render(request,'authentication/profile.html')  
          else:
             messages.success(request,'User with the entered email already exists!!!')
             return render(request,'authentication/signup.html')
     else:        
        return render(request,'authentication/signup.html')

def Profile(request):
     return render(request,"authentication/profile.html")

# Create your views here.
