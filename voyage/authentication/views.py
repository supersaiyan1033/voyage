from django.shortcuts import render, redirect
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
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
          print(row[0][6])
          if cursor.rowcount ==1:
             dbpassword = row[0][6]
             print(dbpassword)
             if bcrypt.checkpw(password.encode('utf8'),dbpassword.encode('utf8')):
                 print('user exists login successfully')
                 return render(request,'user/user.html')
             else:
               print('incorrect password')
          else:
            print('invalid credentials')
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
          cursor.execute("""INSERT INTO users (firstname,lastname,gender,address,mobileno,email,password,DOB) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""", (firstname ,lastname,gender,address,mobileno,email,password,DOB))
          return render(request,'authentication/signup.html')    
     else:        
        return render(request,'authentication/signup.html')


# Create your views here.
