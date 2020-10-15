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
          data={
             'firstname':row[0][0],
             'lastname':row[0][1],
             'gender':row[0][2],
             'address':row[0][3],
             'mobileno':row[0][4],
             'email':row[0][5],
             'password':row[0][6],
             'userId':row[0][7],
             'DOB':row[0][8],
          }
          
          if cursor.rowcount ==1:
             dbpassword = row[0][6]
             print(dbpassword)
             if bcrypt.checkpw(password.encode('utf8'),dbpassword.encode('utf8')):
                 messages.success(request,'Login successful!!')
                 url="{}/{}".format(data["userId"],data["email"])
                 return redirect(url)
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
             messages.success(request,'Singned Up successfully!')
             return redirect('http://127.0.0.1:8000/login')  
          else:
             messages.success(request,'User with the entered email already exists!!!')
             return render(request,'authentication/signup.html')
     else:        
        return render(request,'authentication/signup.html')

def user(request,userId,email):

   return render(request,'authentication/user.html',{'userId':userId,'email':email})


def Profile(request,userId,email):
     cursor = connection.cursor()
     cursor.execute("""SELECT * FROM users WHERE email= %s""",[email])
     row = cursor.fetchall()
    
     data={
             'firstname':row[0][0],
             'lastname':row[0][1],
             'gender':row[0][2],
             'address':row[0][3],
             'mobileno':row[0][4],
             'email':row[0][5],
             'password':row[0][6],
             'userId':row[0][7],
             'DOB':row[0][8],
     }
     if request.method=="POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        DOB = request.POST.get('DOB')
        mobileno = request.POST.get('mobileno')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if bcrypt.checkpw(password.encode('utf8'),data['password'].encode('utf8')):
           messages.success(request,'Profile is Updated Successfully!')
           cursor.execute("""UPDATE users SET firstname=%s,lastname=%s,gender=%s,address=%s,mobileno=%s,email=%s WHERE userId=%s """, (firstname ,lastname,gender,address,mobileno,email,data['userId']))
           return redirect('http://127.0.0.1:8000/login/{}/{}/profile'.format(data["userId"],data["email"]))
        else:
           messages.success(request,'incorrect password please try again!!')
           return render(request,'authentication/profile.html',data)
     else:
        return render(request,"authentication/profile.html",data)


# Create your views here.
