from django.shortcuts import render, redirect
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
from django.contrib import messages
import bcrypt
import hashlib, sys
import base64
from datetime import datetime

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
             messages.success(request,'Sign Up successful!')
             return redirect('http://127.0.0.1:8000/login') 
          else:
             messages.success(request,'User with the entered email already exists!!!')
             return render(request,'authentication/signup.html')
     else:        
        return render(request,'authentication/signup.html')

def user(request,userId,email):
   cursor = connection.cursor()
   cursor.execute("""SELECT * FROM users WHERE email= %s""",[email])
   row = cursor.fetchall()
   data={
             'firstname':row[0][0],
             'mobileno':row[0][4],
             'email':row[0][5],
             'userId':row[0][7],
             'wallet':row[0][9]
     }


   return render(request,'authentication/user.html',data)


def Profile(request,userId,email):
     cursor = connection.cursor()
     cursor.execute("""SELECT * FROM users WHERE email= %s""",[email])
     row = cursor.fetchall()
    
     dateOfBirth = row[0][8].strftime("%Y-%m-%d")
     data={
             'firstname':row[0][0],
             'lastname':row[0][1],
             'gender':row[0][2],
             'address':row[0][3],
             'mobileno':row[0][4],
             'email':row[0][5],
             'password':row[0][6],
             'userId':row[0][7],
             'DOB':dateOfBirth,
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
           cursor.execute("""UPDATE users SET firstname=%s,lastname=%s,gender=%s,address=%s,mobileno=%s,email=%s,DOB=%s WHERE userId=%s """, (firstname ,lastname,gender,address,mobileno,email,DOB,data['userId']))
           return redirect('http://127.0.0.1:8000/login/{}/{}'.format(data["userId"],data["email"]))
        else:
           messages.success(request,'incorrect password please try again!!')
           return render(request,'authentication/profile.html',data)
     else:
        return render(request,"authentication/profile.html",data)

 
def ChangePassword(request,userId,email):
     cursor = connection.cursor()
     cursor.execute("""SELECT * FROM users WHERE email= %s """,[email])
     row = cursor.fetchall()
     dbPassword = row[0][6]
     if request.method=="POST":
        oldPassword = request.POST.get('oldpassword')
        newPassword = request.POST.get('newpassword')
        confirmPassword = request.POST.get('confirmpassword')
        if bcrypt.checkpw(oldPassword.encode('utf8'),dbPassword.encode('utf8')):
           if newPassword ==confirmPassword:
              dbPassword = bcrypt.hashpw(newPassword.encode('utf8'), bcrypt.gensalt(rounds=12))
              cursor.execute("""UPDATE users SET password=%s WHERE email=%s""",(dbPassword,email))
              messages.success(request,'Password changed successfully!')
              return redirect('http://127.0.0.1:8000/login/{}/{}'.format(userId,email))
           else:
              messages.success(request,'new password and confirm password must be the same!!')
              return render(request,'authentication/changepassword.html')
        else:
            messages.success(request,'incorrect password!!')
            return render(request,'authentication/changepassword.html')



     else:
        return render(request,'authentication/changepassword.html')



def Flights(request):
     return render(request,'authentication/flights.html')        
# Create your views here.
