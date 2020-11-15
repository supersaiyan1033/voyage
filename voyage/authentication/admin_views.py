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

def admin(request):
    userId=request.session.get('userId')
    email=request.session.get('email')
    if  request.session.get('role')=='admin':
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE userID= %s""", [userId])
        row = cursor.fetchall()
        dateOfBirth = row[0][8].strftime("%Y-%m-%d")
        data={
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
        return render(request, 'authentication/admin.html', data)
    elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
    else:
        return render(request,'authentication/error.html')

def Admin_Flights(request):
    userId=request.session.get('userId')
    email=request.session.get('email')
    if  request.session.get('role')=='admin':
        
            data={
                'email':email,
                'userId':userId
            }
            return render(request, 'authentication/admin_flights.html',data)

    elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
    else:
        return render(request,'authentication/error.html')

def Admin_Flights_List(request):
    userId=request.session.get('userId')
    email=request.session.get('email')
    if  request.session.get('role')=='admin':
        flight_id = request.GET.get('flight_id')
        cursor = connection.cursor()
        if flight_id==None:
         cursor.execute("""SELECT * FROM flight""")
        else:
         cursor.execute("""SELECT * FROM flight WHERE Flight_ID=%s""",[flight_id])
        row = cursor.fetchall()
        flights=[]
        a = cursor.rowcount
        if a!=0:
         for n in range(a):
             flights.append({
                 'id':row[n][0],
                 'company':row[n][1],
                 'name':row[n][2],
                 'capacity':row[n][3]
             })

         data = {
            'flights':flights,
            'flight_id':flight_id,
            'userId':userId,
            'email':email
         }
         
        else:
            data={
                'flights':None,
                'flight_id':flight_id,
                'userId':userId,
                'email':email
            }
        if request.method=='POST':
            Flight_id = request.POST.get('Flight_id')
            Flight_name = request.POST.get('Flight_name')
            Flight_capacity =request.POST.get('seat_capacity')
            cursor.execute("""SELECT * FROM flight WHERE Flight_ID=%s""",[int(Flight_id)])
            if cursor.rowcount!=0:
             messages.success(request,'flight with the entered flight id already exists!!')
             return render(request,'authentication/admin_flights_list.html',data)
            else:
                
                cursor.execute("""INSERT INTO flight (Flight_ID,Company,Flight_name,seat_Capacity) VALUES (%s,%s,%s,%s)""",(int(Flight_id),'Voyage',Flight_name,int(Flight_capacity)))
                messages.success(request,'flight added successfully')
                return redirect('http://127.0.0.1:8000/admin/home')
        else:
         return render(request,'authentication/admin_flights_list.html',data)
    elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
    else:
        return render(request,'authentication/error.html')

def Admin_Flights_Details(request):
    userId=request.session.get('userId')
    email=request.session.get('email')
    if  request.session.get('role')=='admin':
        flight_no = request.GET.get('flight_no')
        cursor = connection.cursor()
        from_p_list =[]
        cursor.execute("""SELECT DISTINCT from_p FROM route""")
        row =cursor.fetchall()
        a = cursor.rowcount
        for n in range(a):
            from_p_list.append(row[n][0])
        to_p_list = []
        cursor.execute("""SELECT DISTINCT to_p FROM route""")
        row = cursor.fetchall()
        a = cursor.rowcount
        for n in range(a):
            to_p_list.append(row[n][0])
        if flight_no==None:
         cursor.execute("""SELECT * FROM flight_details JOIN route on flight_details.RID = route.RID""")
        else:
         cursor.execute("""SELECT * FROM flight_details JOIN route on flight_details.RID = route.RID WHERE Flight_No=%s""",[flight_no])
        row = cursor.fetchall()
        flights=[]
        a = cursor.rowcount
        if a!=0:
         for n in range(a):
             flights.append({
                 'id':row[n][0],
                 'from_time':row[n][1],
                 'to_time':row[n][2],
                 'price':row[n][3],
                 'no':row[n][4],
                 'from_p':row[n][7],
                 'to_p':row[n][8]
             })

         data = {
            'flights':flights,
            'from_p_list':from_p_list,
            'to_p_list':to_p_list,
            'flight_no':flight_no,
            'userId':userId,
            'email':email
         }
         
        else:
            data={
                'flights':None,
                'from_p_list':from_p_list,
                'to_p_list':to_p_list,
                'flight_no':flight_no,
                'userId':userId,
                'email':email

            }
        if request.method=='POST':
            Flight_id = request.POST.get('Flight_id')
            time_from = request.POST.get('time_from')
            time_to =request.POST.get('time_to')
            flight_no = request.POST.get('Flight_no')
            starting_point = request.POST.get('starting_point')
            destination_point = request.POST.get('destination_point')
            price = request.POST.get('price')
            cursor.execute("""SELECT RID FROM route WHERE from_p =%s AND to_p =%s""",(starting_point,destination_point))
            row = cursor.fetchall()
            if cursor.rowcount==0:
                messages.success(request,'the entered route does not exist please add route first!!')
                return redirect('http://127.0.0.1:8000/admin/routes')
            else:
              rid = row[0][0]
              cursor.execute("""SELECT * FROM flight WHERE Flight_ID=%s""",[Flight_id])
              if cursor.rowcount==0:
                  messages.success(request,'flight does not exist please add the flight!!')
                  return redirect('http://127.0.0.1:8000/admin/flights/list')
              else:
               cursor.execute("""SELECT * FROM flight_details WHERE Flight_ID=%s AND Time_From=%s AND Time_To=%s AND Price=%s AND Flight_No=%s AND RID=%s""",(int(Flight_id),time_from,time_to,int(price),int(flight_no),int(row[0][0])))
               if cursor.rowcount!=0:
                messages.success(request,'flight details already exists!!')
                return render(request,'authentication/admin_flights_details.html',data)
               else:
                
                cursor.execute("""INSERT INTO flight_details (Flight_ID,Time_From,Time_To,Price,Flight_No,RID) VALUES (%s,%s,%s,%s,%s,%s)""",(int(Flight_id),time_from,time_to,int(price),int(flight_no),rid))
                messages.success(request,'flight details added successfully')
                return redirect('http://127.0.0.1:8000/admin/home')
        else:
         return render(request,'authentication/admin_flights_details.html',data)
           

    elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
    else:
        return render(request,'authentication/error.html')



def Admin_Flights_Schedule(request):
 userId=request.session.get('userId')
 email=request.session.get('email')   
 if request.session.get('role')=='admin':
     date_filter = request.GET.get('date_from')
     cursor = connection.cursor()
     if date_filter==None:
         cursor.execute("""SELECT flight_schedule.Flight_No,date_from,date_to,seat_Capacity FROM flight_schedule JOIN flight_details ON flight_schedule.Flight_No = flight_details.Flight_No JOIN flight ON flight_details.Flight_ID = flight.Flight_ID """)
     else:
         cursor.execute("""SELECT flight_schedule.Flight_No,date_from,date_to,seat_Capacity FROM flight_schedule JOIN flight_details ON flight_schedule.Flight_No = flight_details.Flight_No JOIN flight ON flight_details.Flight_ID = flight.Flight_ID WHERE date_from=%s""",[date_filter])
     row = cursor.fetchall()
     schedules=[]
     a = cursor.rowcount
     if a!=0:
         for n in range(a):
          schedules.append({
            'flight_no':row[n][0],
            'date_from':row[n][1],
            'date_to':row[n][2],
            'seats':row[n][3]
          })
         data={
         'schedules':schedules,
         'date_filter':date_filter,
         'userId':userId,
         'email':email
          }
     else:
         data={
           'schedules':None,
           'date_filter':date_filter,
           'userId':userId,
           'email':email
         }
     if request.method=='POST':
         flight_no = request.POST.get('Flight_No')
         date_from = request.POST.get('date_from')
         date_to   = request.POST.get('date_to')
         cursor.execute("""SELECT * FROM flight_details WHERE Flight_No=%s""",[flight_no])
         if cursor.rowcount==0:
             messages.success(request,'flight with the entered flight number does not exist please add flight details first!! ')
             return redirect('http://127.0.0.1:8000/admin/flights/details')
         else:
             cursor.execute("""SELECT seat_Capacity FROM flight_details JOIN flight ON flight.Flight_ID= flight_details.Flight_ID WHERE Flight_No=%s""",[flight_no])
             row = cursor.fetchall()
             seats= row[0][0]
             cursor.execute("""SELECT Time_From,Time_To FROM flight_details  WHERE flight_details.Flight_No =%s""",[flight_no])
             row = cursor.fetchall()
             now = datetime.now()
             now = now.strftime("%Y-%m-%d %H:%M:%S")
             time_from_db = row[0][0].strftime("%H:%M:%S")
             time_to_db = row[0][1].strftime("H:%M:%S")
             date_time_from_db = date_from+' '+time_from_db
             date_time_to_db = date_to+' '+time_to_db
             if date_time_from_db<now or date_time_to_db<date_time_from_db :
                 messages.success(request,'you cannot add a flight schedule in the past')
                 return redirect('http://127.0.0.1:8000/admin/flights/schedule')
             else:
               cursor.execute("""SELECT * FROM flight_schedule WHERE Flight_No =%s AND date_from =%s AND date_to=%s AND no_of_seats_vacant=%s""",(flight_no,date_from,date_to,int(seats)))
               if cursor.rowcount!=0:
                   messages.success(request,'flight schedule already exists!!')
                   return redirect('http://127.0.0.1:8000/admin/flights/schedule')
               else:
                cursor.execute("""INSERT INTO flight_schedule (Flight_No,date_from,date_to,no_of_seats_vacant) VALUES(%s,%s,%s,%s)""",(flight_no,date_from,date_to,int(seats)))
                messages.success(request,'flight schedule added successfully')
                return redirect('http://127.0.0.1:8000/admin/flights/schedule')

     else:
         return render(request,'authentication/admin_flights_schedule.html',data)
 elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
 else:
        return render(request,'authentication/error.html')


def Admin_Buses(request):
    userId=request.session.get('userId')
    email=request.session.get('email')
    if  request.session.get('role')=='admin':
      
            data={
                'email':email,
                'userId':userId
            }
            return render(request, 'authentication/admin_buses.html',data)
    elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
    else:
        return render(request,'authentication/error.html')



def Admin_Routes(request):
      userId=request.session.get('userId')
      email=request.session.get('email')
      if  request.session.get('role')=='admin':
        start = request.GET.get('from_p')
        end = request.GET.get('to_p')
        cursor = connection.cursor()
        if start==None:
         cursor.execute("""SELECT * FROM route""")
        else:
         cursor.execute("""SELECT * FROM route WHERE from_p=%s AND to_p=%s""",(start,end))
        row = cursor.fetchall()
        routes=[]
        a = cursor.rowcount
        if a!=0:
         for n in range(a):
             routes.append({
                 'no':n+1,
                 'RID':row[n][0],
                 'from_p':row[n][1],
                 'to_p':row[n][2]
             })

         data = {
            'routes':routes,
            'start':start,
            'end':end,
            'userId':userId,
            'email':email
         }
         
        else:
            data={
                'routes':None,
                'start':start,
                'end':end,
                'userId':userId,
                'email':email
            }
        if request.method=='POST':
            start = request.POST.get('from_p')
            end = request.POST.get('to_p')
            cursor.execute("""SELECT * FROM route WHERE from_p=%s AND to_p=%s""",(start,end))
            if cursor.rowcount!=0:
             messages.success(request,'route already exists!!')
             return render(request,'authentication/admin_routes.html',data)
            else:
                cursor.execute("""INSERT INTO route (from_p,to_p) VALUES (%s,%s)""",(start,end))
                messages.success(request,'route added successfully')
                return redirect('http://127.0.0.1:8000/admin/home')
        else:
         return render(request,'authentication/admin_routes.html',data)
      elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
      else:
        return render(request,'authentication/error.html')

def Admin_Buses_List(request):
    userId=request.session.get('userId')
    email=request.session.get('email')
    if  request.session.get('role')=='admin':
        bus_id = request.GET.get('bus_id')
        cursor = connection.cursor()
        if bus_id==None:
         cursor.execute("""SELECT * FROM bus""")
        else:
         cursor.execute("""SELECT * FROM bus WHERE Bus_ID=%s""",[bus_id])
        row = cursor.fetchall()
        buses=[]
        a = cursor.rowcount
        if a!=0:
         for n in range(a):
             buses.append({
                 'id':row[n][0],
                 'company':row[n][1],
                 'name':row[n][2],
                  'capacity':row[n][3]
             })

         data = {
            'buses':buses,
            'bus_id':bus_id,
            'userId':userId,
            'email':email
         }
         
        else:
            data={
                'buses':None,
                'bus_id':bus_id,
                'userId':userId,
                'email':email
            }
        if request.method=='POST':
            Bus_id = request.POST.get('Bus_id')
            Bus_name = request.POST.get('Bus_name')
            Bus_capacity =request.POST.get('seat_capacity')
            cursor.execute("""SELECT * FROM bus WHERE Bus_ID=%s""",[int(Bus_id)])
            if cursor.rowcount!=0:
             messages.success(request,'bus already exists!!')
             return render(request,'authentication/admin_buses_list.html',data)
            else:
                
                cursor.execute("""INSERT INTO bus(Bus_ID,Company,Bus_name,seat_Capacity) VALUES (%s,%s,%s,%s)""",(int(Bus_id),'Voyage',Bus_name,int(Bus_capacity)))
                messages.success(request,'Bus added successfully')
                return redirect('http://127.0.0.1:8000/admin/home')
        else:
         return render(request,'authentication/admin_buses_list.html',data)
    elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
    else:
        return render(request,'authentication/error.html') 

def Admin_Buses_Details(request):
    userId=request.session.get('userId')
    email=request.session.get('email')
    if  request.session.get('role')=='admin':
        bus_no = request.GET.get('bus_no')
        cursor = connection.cursor()
        from_p_list =[]
        cursor.execute("""SELECT DISTINCT from_p FROM route""")
        row =cursor.fetchall()
        a = cursor.rowcount
        for n in range(a):
            from_p_list.append(row[n][0])
        to_p_list = []
        cursor.execute("""SELECT DISTINCT to_p FROM route""")
        row = cursor.fetchall()
        a = cursor.rowcount
        for n in range(a):
            to_p_list.append(row[n][0])
        if bus_no==None:
         cursor.execute("""SELECT * FROM bus_details JOIN route on bus_details.RID = route.RID""")
        else:
         cursor.execute("""SELECT * FROM bus_details JOIN route on bus_details.RID = route.RID WHERE Bus_No=%s""",[bus_no])
        row = cursor.fetchall()
        buses=[]
        a = cursor.rowcount
        if a!=0:
         for n in range(a):
             buses.append({
                 'id':row[n][0],
                 'from_time':row[n][1],
                 'to_time':row[n][2],
                 'price':row[n][3],
                 'no':row[n][4],
                 'from_p':row[n][7],
                 'to_p':row[n][8]
             })

         data = {
            'buses':buses,
            'from_p_list':from_p_list,
            'to_p_list':to_p_list,
            'bus_no':bus_no,
            'userId':userId,
            'email':email
         }
         
        else:
            data={
                'buses':None,
                'from_p_list':from_p_list,
                'to_p_list':to_p_list,
                'bus_no':bus_no,
                'userId':userId,
                'email':email

            }
        if request.method=='POST':
            Bus_id = request.POST.get('Bus_id')
            time_from = request.POST.get('time_from')
            time_to =request.POST.get('time_to')
            bus_no = request.POST.get('Bus_no')
            starting_point = request.POST.get('starting_point')
            destination_point = request.POST.get('destination_point')
            price = request.POST.get('price')
            cursor.execute("""SELECT RID FROM route WHERE from_p =%s AND to_p =%s""",(starting_point,destination_point))
            row = cursor.fetchall()
            if cursor.rowcount==0:
                messages.success(request,'the entered route does not exist, please add route first!!')
                return redirect('http://127.0.0.1:8000/admin/routes')
            else:
              rid = row[0][0]
              cursor.execute("""SELECT * FROM bus WHERE Bus_ID=%s""",[Bus_id])
              if cursor.rowcount==0:
                  messages.success(request,'bus does not exist witht he entered bus id please add bus!!')
                  return redirect('http://127.0.0.1:8000/admin/buses/list')
              else:
               cursor.execute("""SELECT * FROM bus_details WHERE Bus_ID=%s AND Time_From=%s AND Time_To=%s AND Price=%s AND Bus_No=%s AND RID=%s""",(int(Bus_id),time_from,time_to,int(price),int(bus_no),int(row[0][0])))
               if cursor.rowcount!=0:
                messages.success(request,'bus details already exists!!')
                return render(request,'authentication/admin_buses_details.html',data)
               else:
                
                cursor.execute("""INSERT INTO bus_details (Bus_ID,Time_From,Time_To,Price,Bus_No,RID) VALUES (%s,%s,%s,%s,%s,%s)""",(int(Bus_id),time_from,time_to,int(price),int(bus_no),rid))
                messages.success(request,'bus details added successfully')
                return redirect('http://127.0.0.1:8000/admin/home')
        else:
         return render(request,'authentication/admin_buses_details.html',data)
           

    elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
    else:
        return render(request,'authentication/error.html') 

def Admin_Buses_Schedule(request):
 userId=request.session.get('userId')
 email=request.session.get('email')
 if  request.session.get('role')=='admin':
     date_filter = request.GET.get('date_from')
     cursor = connection.cursor()
     if date_filter==None:
         cursor.execute("""SELECT bus_schedule.Bus_No,date_from,date_to,seat_Capacity FROM bus_schedule JOIN bus_details ON bus_schedule.Bus_No = bus_details.Bus_No JOIN bus ON bus_details.Bus_ID = bus.Bus_ID """)
     else:
         cursor.execute("""SELECT bus_schedule.Bus_No,date_from,date_to,seat_Capacity FROM bus_schedule JOIN bus_details ON bus_schedule.Bus_No = bus_details.Bus_No JOIN bus ON bus_details.Bus_ID = bus.Bus_ID  WHERE date_from=%s""",[date_filter])
     row = cursor.fetchall()
     schedules=[]
     a = cursor.rowcount
     if a!=0:
         for n in range(a):
          schedules.append({
            'bus_no':row[n][0],
            'date_from':row[n][1],
            'date_to':row[n][2],
            'seats':row[n][3]
          })
         data={
         'schedules':schedules,
         'date_filter':date_filter,
         'userId':userId,
         'email':email
          }
     else:
         data={
           'schedules':None,
           'date_filter':date_filter,
           'userId':userId,
           'email':email
         }
     if request.method=='POST':
         bus_no = request.POST.get('Bus_No')
         date_from = request.POST.get('date_from')
         date_to   = request.POST.get('date_to')
         cursor.execute("""SELECT * FROM bus_details WHERE Bus_No=%s""",[bus_no])
         if cursor.rowcount==0:
             messages.success(request,'bus with the entered bus number does not exist, please add the bus no in the bus details first!!')
             return redirect('http://127.0.0.1:8000/admin/buses/details')
         else:
             cursor.execute("""SELECT seat_Capcaity FROM bus_details JOIN bus ON bus_details.Bus_ID= bus.Bus_ID WJHERE Bus_No = %s""",[bus_no])
             row = cursor.fetchall()
             seats = row[0][0]
             cursor.execute("""SELECT Time_From,Time_To FROM bus_details  WHERE bus_details.Bus_No =%s""",[bus_no])
             row = cursor.fetchall()
             now = datetime.now()
             now = now.strftime("%Y-%m-%d %H:%M:%S")
             time_from_db = row[0][0].strftime("%H:%M:%S")
             time_to_db = row[0][1].strftime("H:%M:%S")
             date_time_from_db = date_from+' '+time_from_db 
             date_time_to_db = date_to+' '+time_to_db
             if date_time_from_db<now or date_time_from_db>date_time_to_db:
                 messages.success(request,'you cannot add a bus schedule in the past')
                 return redirect('http://127.0.0.1:8000/admin/buses/schedule')
             else:
               cursor.execute("""SELECT * FROM bus_schedule WHERE Bus_No=%s AND date_from=%s AND date_to=%s AND no_of_seats_vacant=%s""",(bus_no,date_from,date_to,int(seats)))
               if cursor.rowcount!=0:
                   messages.success(request,'Bus schedule already exists!!')
                   return redirect('http://127.0.0.1:8000/admin/buses/schedule')
               else:
                cursor.execute("""INSERT INTO bus_schedule (Bus_No,date_from,date_to,no_of_seats_vacant) VALUES(%s,%s,%s,%s)""",(bus_no,date_from,date_to,int(seats)))
                messages.success(request,'bus schedule added successfully')
                return redirect('http://127.0.0.1:8000/admin/home')
          

     else:
         return render(request,'authentication/admin_buses_schedule.html',data)
 elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
 else:
        return render(request,'authentication/error.html')

def View_Admin(request):
   if  request.session.get('role')=='admin':
    email = request.GET.get('email')
    cursor= connection.cursor()
    if email == None:
        cursor.execute("""SELECT firstname,lastname,email,role FROM users""")
    else:
        cursor.execute("""SELECT firstname,lastname,email,role FROM users WHERE email=%s""",[email])
    row = cursor.fetchall()
    a = cursor.rowcount
    users = []
    for n in range(a):
         users.append({
            'firstname':row[n][0],
            'lastname':row[n][1],
            'email':row[n][2],
            'role':row[n][3]
         })
    if len(users)!=0:
        data={
            'users':users
        }
    else:
        data={
            'users':None
        }
    if request.method =='POST':
        role = request.POST.get('role')
        email_id = request.POST.get('email_id')
        cursor.execute("""UPDATE users SET role=%s WHERE email=%s""",(role,email_id))
        messages.success(request,"role of the user has been updated successfully!!")
        return redirect('http://127.0.0.1:8000/admin/home')
    else:
        return render(request,'authentication/admin_add_admin.html',data)
   elif request.session.get('email')!=None:
       return render(request,'authentication/page_not_found.html')
   else:
       return render(request,'authentication/error.html')



