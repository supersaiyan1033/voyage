from django.shortcuts import render, redirect
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
from django.contrib import messages
import bcrypt
import hashlib
import sys
import base64
from datetime import datetime
from datetime import date
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import smtplib
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.utils.crypto import get_random_string
def myFunc(e):
  return e['date_of_booking']

# authentication views starts here

def Home(request):
    if request.session.get('email')!=None:
        email = request.session.get('email')
        userId = request.session.get('userId')
        role=request.session.get('role')
        if role=="user":
            url ="http://127.0.0.1:8000/home"
        else:
            url="http://127.0.0.1:8000/admin/home"    
        return redirect(url)
    else:
      return render(request, 'authentication/home.html')



def About_us(request):
    return render(request,'authentication/about_us.html')

def Contact_us(request):
    if request.method =='POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        message = request.POST.get('message')
        cursor = connection.cursor()
        cursor.execute("""SELECT email FROM users WHERE role=%s""",['admin'])
        a = cursor.rowcount
        row = cursor.fetchall()
        admins = []
        for n in range(a):
           admins.append(row[n][0])

        send_mail(subject='Contact us',from_email='cse190001033@iiti.ac.in',recipient_list=admins,html_message='<h4>from:{}</h4><br><h4>to:cse190001033@iiti.ac.in</h4><br><h3>{}</h3>'.format(email,message),message=message)
        messages.success(request,'sent successfully')
        return render(request,'authentication/contact_us.html')
    else:
     return render(request,'authentication/contact_us.html')


def Log_In(request):
    request.session.flush()
    request.session.clear_expired()
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE email= %s""", [email])
        row = cursor.fetchall()
        if cursor.rowcount == 1:
            dbpassword = row[0][6]
            userId = row[0][7]
            data = {
            'firstname': row[0][0],
            'lastname': row[0][1],
            'gender': row[0][2],
            'address': row[0][3],
            'mobileno': row[0][4],
            'email': row[0][5],
            'password': row[0][6],
            'userId': row[0][7],
            'DOB': row[0][8],
            'role':row[0][10]
             }
            if bcrypt.checkpw(password.encode('utf8'), dbpassword.encode('utf8')):
               
                request.session['userId'] = row[0][7]
                if data["role"]=="admin":
                    messages.success(request, 'Login successful!!')
                    request.session['email'] = email
                    request.session['role'] = data['role']
                    url = "http://127.0.0.1:8000/admin/home"
                    return redirect(url)
                elif data["role"]=='user':
                    messages.success(request, 'Login successful!!')
                    request.session['email'] = email
                    request.session['role'] = data['role']
                    url="http://127.0.0.1:8000/home"
                    return redirect(url)
               
            else:
              
                 messages.success(request, 'incorrect password please try again!!')
                 return render(request, 'authentication/login.html')
        else:
            messages.success(request, 'Account does not exist with the entered credentials!! signup to create an account')
            return render(request, 'authentication/login.html')
    else:
        return render(request, 'authentication/login.html')


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
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE email = %s""", [email])
        row = cursor.fetchall()
        if cursor.rowcount == 0:
            request.session['firstname'] = firstname
            request.session['lastname'] = lastname
            request.session['gender'] = gender
            request.session['address'] = address
            request.session['DOB'] = DOB
            request.session['mobileno'] = mobileno
            request.session['email'] = email
            request.session['password'] = password
            otp = get_random_string(6, allowed_chars='0123456789')
            request.session['otp'] = otp
            send_mail(subject='{} is your Pack your bags OTP'.format(otp),message='click on the below link to Verify your email.Note that this link will only be active for 10minutes.',from_email='cse190001033@iiti.ac.in',recipient_list=[email],fail_silently=True,
            html_message="<h2>Please enter the below OTP to complete your verification.Note that this OTP will only be active for 10minutes.</h2><br><h2>{}</h2>".format(otp))
            request.session['email_link_is_active'] = True
            messages.success(request,'OTP sent to your email please check your inbox!!')
            return redirect('http://127.0.0.1:8000/login/emailverification')
        else:
            messages.success(
                request, 'User with the entered email already exists please login to continue!!!')
            return redirect('http://127.0.0.1:8000/login')
            

    else:
        return render(request, 'authentication/signup.html')

def Verify_User_by_website(request):
 if request.session.get('email_link_is_active'):
    if request.method =='POST':
        otp = request.POST.get('otp')
        cursor = connection.cursor()
        if request.session.get('otp')!=None:
         otp_from_email = request.session.get('otp')
         if otp == otp_from_email:
             firstname = request.session.get('firstname')
             lastname = request.session.get('lastname')
             email = request.session.get('email')
             DOB = request.session.get('DOB')
             gender = request.session.get('gender')
             address = request.session.get('address')
             mobileno = request.session.get('mobileno')
             password = request.session.get('password')
             password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(rounds=12))
             cursor.execute("""INSERT INTO users(firstname,lastname,gender,address,DOB,mobileno,email,password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(firstname,lastname,gender,address,DOB,mobileno,email,password))
             messages.success(request,'verification successful!!please  login to continue')
             return redirect('http://127.0.0.1:8000/login')
         else:
             messages.success(request,'invalid otp try again!!')
             return redirect('http://127.0.0.1:8000/login/emailverification')

        else:
            messages.success(request,'Signup before email verification!!')
            return redirect('http://127.0.0.1:8000/signup')
    else:
        return render(request,'authentication/verify_email.html')
 else:
     return render(request,'authentication/error.html')






def user(request):
 userId=request.session.get('userId')
 email=request.session.get('email')
 if request.session.get('email')==email and request.session.get('role')=='user':
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM users WHERE email= %s""", [email])
    row = cursor.fetchall()
    dateOfBirth = row[0][8].strftime("%Y-%m-%d")
    data = {
        'firstname': row[0][0],
        'lastname': row[0][1],
        'gender': row[0][2],
        'address': row[0][3],
        'mobileno': row[0][4],
        'email': row[0][5],
        'password': row[0][6],
        'userId': row[0][7],
        'DOB': dateOfBirth,
        'wallet': row[0][9]
    }

    return render(request, 'authentication/user.html', data)
 elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
 else:
        return render(request,'authentication/error.html')





def Profile(request):
 userId=request.session.get('userId')
 email=request.session.get('email')
 if request.session.get('email') == email:
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM users WHERE email= %s""", [email])
    row = cursor.fetchall()
    genders = ['Male', 'Female', 'Others']

    dateOfBirth = row[0][8].strftime("%Y-%m-%d")
    data = {
        'firstname': row[0][0],
        'lastname': row[0][1],
        'gender': row[0][2],
        'address': row[0][3],
        'mobileno': row[0][4],
        'email': row[0][5],
        'password': row[0][6],
        'userId': row[0][7],
        'DOB': dateOfBirth,
        'genders': genders
    }
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        DOB = request.POST.get('DOB')
        mobileno = request.POST.get('mobileno')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if bcrypt.checkpw(password.encode('utf8'), data['password'].encode('utf8')):
            messages.success(request, 'Profile is Updated Successfully!')
            cursor.execute("""UPDATE users SET firstname=%s,lastname=%s,gender=%s,address=%s,mobileno=%s,email=%s,DOB=%s WHERE userId=%s """,
                           (firstname, lastname, gender, address, mobileno, email, DOB, data['userId']))
            return redirect('http://127.0.0.1:8000/home')
        else:
            messages.success(request, 'incorrect password please try again!!')
            return render(request, 'authentication/profile.html', data)
    else:
        return render(request, "authentication/profile.html", data)
 else:
     return render(request,'authentication/error.html')


def ChangePassword(request):
 userId=request.session.get('userId')
 email=request.session.get('email')   
 if request.session.get('email') == email:
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM users WHERE email= %s """, [email])
    row = cursor.fetchall()
    dbPassword = row[0][6]
    if request.method == "POST":
        oldPassword = request.POST.get('oldpassword')
        newPassword = request.POST.get('newpassword')
        confirmPassword = request.POST.get('confirmpassword')
        if bcrypt.checkpw(oldPassword.encode('utf8'), dbPassword.encode('utf8')):
            if newPassword == confirmPassword:
                dbPassword = bcrypt.hashpw(newPassword.encode(
                    'utf8'), bcrypt.gensalt(rounds=12))
                cursor.execute(
                    """UPDATE users SET password=%s WHERE email=%s""", (dbPassword, email))
                messages.success(request, 'Password changed successfully!')
                return redirect('http://127.0.0.1:8000/home')
            else:
                messages.success(
                    request, 'new password and confirm password must be the same!!')
                return render(request, 'authentication/changepassword.html')
        else:
            messages.success(request, 'incorrect password!!')
            return render(request, 'authentication/changepassword.html')

    else:
        return render(request, 'authentication/changepassword.html')
 else:
     return render(request,'authentication/error.html')

def Admin_ChangePassword(request):
    userId=request.session.get('userId')
    email=request.session.get('email')
    if request.session.get('email') ==email:
     cursor = connection.cursor()
     cursor.execute("""SELECT * FROM users WHERE email= %s """, [email])
     row = cursor.fetchall()
     dbPassword = row[0][6]
     if request.method == "POST":
        oldPassword = request.POST.get('oldpassword')
        newPassword = request.POST.get('newpassword')
        confirmPassword = request.POST.get('confirmpassword')
        if bcrypt.checkpw(oldPassword.encode('utf8'), dbPassword.encode('utf8')):
            if newPassword == confirmPassword:
                dbPassword = bcrypt.hashpw(newPassword.encode(
                    'utf8'), bcrypt.gensalt(rounds=12))
                cursor.execute(
                    """UPDATE users SET password=%s WHERE email=%s""", (dbPassword, email))
                messages.success(request, 'Password changed successfully!')
                return redirect('http://127.0.0.1:8000/admin/home')
            else:
                messages.success(
                    request, 'new password and confirm password must be the same!!')
                return render(request, 'authentication/changepassword.html')
        else:
            messages.success(request, 'incorrect password!!')
            return render(request, 'authentication/changepassword.html')

     else:
        return render(request, 'authentication/changepassword.html')
    else:
     return render(request,'authentication/error.html')


def Forgot_Password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE email= %s""", [email] )
        if cursor.rowcount==1:
            send_mail(subject='reset password request',message='click on the below link to reset your password.Note that this link will only be active for 10minutes.',from_email='cse190001033@iiti.ac.in',recipient_list=[email],fail_silently=False,
            html_message="<h1> click on the below link to reset your password.Note that this link will only be active for 10minutes.</h1><br><a href='http://127.0.0.1:8000/login/forgotpassword/{}/resetpassword'>to reset your password click here</a>".format(email))
            request.session['link_is_active'] = True
            messages.success(request,'rest link sent to the entered mail please check your inbox!!')
            return render(request,'authentication/forgotpassword.html')
        else:
            messages.success(request,'account with the entered email doesnt exist')
            return render(request,'authentication/forgotpassword.html')
    else:
        return render(request,'authentication/forgotpassword.html')
# authentication views ends here flights part begins.

def Reset_Password(request,email):
    if request.session.get('link_is_active'):
        if request.method=='POST':
            newpassword = request.POST.get('newpassword')
            confirmpassword = request.POST.get('confirmpassword')
            if newpassword == confirmpassword:
                cursor = connection.cursor()
                dbPassword = bcrypt.hashpw(newpassword.encode(
                    'utf8'), bcrypt.gensalt(rounds=12))
                cursor.execute(
                    """UPDATE users SET password=%s WHERE email=%s""", (dbPassword, email))
                messages.success(request, 'Password changed successfully!')
                return redirect('http://127.0.0.1:8000/login')
            else:
                messages.success(request,'both fileds must be the same!!')
                return render(request,'authentication/reset_password.html')
                 
        else:
            return render(request,'authentication/reset_password.html')    
    else:
        return render(request,'authentication/error.html')