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

def admin(request,userId,email):
    if request.session.get('email')== email and request.session.get('role')=='admin':
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

def Admin_Flights(request,userId,email):
    if request.session.get('email')== email and request.session.get('role')=='admin':
        
            data={
                'email':email,
                'userId':userId
            }
            return render(request, 'authentication/admin_flights.html',data)

    elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
    else:
        return render(request,'authentication/error.html')

def Admin_Flights_List(request,userId,email):
    if request.session.get('email')== email and request.session.get('role')=='admin':
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
                return redirect('http://127.0.0.1:8000/login/admin/{}/{}'.format(userId,email))
        else:
         return render(request,'authentication/admin_flights_list.html',data)
    elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
    else:
        return render(request,'authentication/error.html')

def Admin_Flights_Details(request,userId,email):
    if request.session.get('email')== email and request.session.get('role')=='admin':
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
                return redirect('http://127.0.0.1:8000/login/admin/{}/{}/routes'.format(userId,email))
            else:
              rid = row[0][0]
              cursor.execute("""SELECT * FROM flight WHERE Flight_ID=%s""",[Flight_id])
              if cursor.rowcount==0:
                  messages.success(request,'flight does not exist please add the flight!!')
                  return redirect('http://127.0.0.1:8000/login/admin/{}/{}/flights/list'.format(userId,email))
              else:
               cursor.execute("""SELECT * FROM flight_details WHERE Flight_ID=%s AND Time_From=%s AND Time_To=%s AND Price=%s AND Flight_No=%s AND RID=%s""",(int(Flight_id),time_from,time_to,int(price),int(flight_no),int(row[0][0])))
               if cursor.rowcount!=0:
                messages.success(request,'flight details already exists!!')
                return render(request,'authentication/admin_flights_details.html',data)
               else:
                
                cursor.execute("""INSERT INTO flight_details (Flight_ID,Time_From,Time_To,Price,Flight_No,RID) VALUES (%s,%s,%s,%s,%s,%s)""",(int(Flight_id),time_from,time_to,int(price),int(flight_no),rid))
                messages.success(request,'flight details added successfully')
                return redirect('http://127.0.0.1:8000/login/admin/{}/{}'.format(userId,email))
        else:
         return render(request,'authentication/admin_flights_details.html',data)
           

    elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
    else:
        return render(request,'authentication/error.html')



def Admin_Flights_Schedule(request,userId,email):
 if request.session.get('email')== email and request.session.get('role')=='admin':
     date_filter = request.GET.get('date_from')
     cursor = connection.cursor()
     if date_filter==None:
         cursor.execute("""SELECT * FROM flight_schedule""")
     else:
         print(date_filter)
         print(date_filter)
         cursor.execute("""SELECT * FROM flight_schedule WHERE date_from=%s""",[date_filter])
     row = cursor.fetchall()
     schedules=[]
     a = cursor.rowcount
     if a!=0:
         for n in range(a):
          schedules.append({
            'flight_no':row[n][0],
            'date_from':row[n][1],
            'date_to':row[n][2],
            'seats':row[n][4]
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
         cursor.execute("""SELECT Time_From,seat_Capacity FROM flight_details JOIN flight_schedule ON flight_details.Flight_No = flight_schedule.Flight_No JOIN flight ON flight.Flight_ID = flight_details.Flight_ID WHERE flight_details.Flight_No =%s""",[flight_no])
         if cursor.rowcount==0:
             messages.success(request,'flight with the entered flight number does not exist please add flight details first!! ')
             return redirect('http://127.0.0.1:8000/login/admin/{}/{}/flights/details'.format(userId,email))
         else:
             now = datetime.now()
             now = now.strftime("%Y-%m-%d %H:%M:%S")
             time_from_db = row[0][1].strftime("%H:%M:%S")
             date_time_db = date_from+' '+time_from_db
             if date_time_db<now:
                 messages.success(request,'you cannot add a flight schedule in the past')
                 return redirect('http://127.0.0.1:8000/login/admin/{}/{}/flights/schedule'.format(userId,email))
             else:
               row = cursor.fetchall()
               seats=row[0][1]
               cursor.execute("""INSERT INTO flight_schedule (Flight_No,date_from,date_to,no_of_seats_vacant,Total_seats) VALUES(%s,%s,%s,%s,%s)""",(flight_no,date_from,date_to,int(seats),int(seats)))
               messages.success(request,'flight schedule added successfully')
               return redirect('http://127.0.0.1:8000/login/admin/{}/{}/flights/schedule'.format(userId,email))
     else:
         return render(request,'authentication/admin_flights_schedule.html',data)
 elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
 else:
        return render(request,'authentication/error.html')


def Admin_Buses(request,userId,email):
    if request.session.get('email')== email and request.session.get('role')=='admin':
      
            data={
                'email':email,
                'userId':userId
            }
            return render(request, 'authentication/admin_buses.html',data)
    elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
    else:
        return render(request,'authentication/error.html')



def Admin_Routes(request,userId,email):
      if request.session.get('email')== email and request.session.get('role')=='admin':
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
                return redirect('http://127.0.0.1:8000/login/admin/{}/{}'.format(userId,email))
        else:
         return render(request,'authentication/admin_routes.html',data)
      elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
      else:
        return render(request,'authentication/error.html')

def Admin_Buses_List(request,userId,email):
    if request.session.get('email')== email and request.session.get('role')=='admin':
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
                return redirect('http://127.0.0.1:8000/login/admin/{}/{}'.format(userId,email))
        else:
         return render(request,'authentication/admin_buses_list.html',data)
    elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
    else:
        return render(request,'authentication/error.html') 

def Admin_Buses_Details(request,userId,email):
    if request.session.get('email')== email and request.session.get('role')=='admin':
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
                return redirect('http://127.0.0.1:8000/login/admin/{}/{}/routes'.format(userId,email))
            else:
              rid = row[0][0]
              cursor.execute("""SELECT * FROM bus WHERE Bus_ID=%s""",[Bus_id])
              if cursor.rowcount==0:
                  messages.success(request,'bus does not exist witht he entered bus id please add bus!!')
                  return redirect('http://127.0.0.1:8000/login/admin/{}/{}/buses/list'.format(userId,email))
              else:
               cursor.execute("""SELECT * FROM bus_details WHERE Bus_ID=%s AND Time_From=%s AND Time_To=%s AND Price=%s AND Bus_No=%s AND RID=%s""",(int(Bus_id),time_from,time_to,int(price),int(bus_no),int(row[0][0])))
               if cursor.rowcount!=0:
                messages.success(request,'bus details already exists!!')
                return render(request,'authentication/admin_buses_details.html',data)
               else:
                
                cursor.execute("""INSERT INTO bus_details (Bus_ID,Time_From,Time_To,Price,Bus_No,RID) VALUES (%s,%s,%s,%s,%s,%s)""",(int(Bus_id),time_from,time_to,int(price),int(bus_no),rid))
                messages.success(request,'bus details added successfully')
                return redirect('http://127.0.0.1:8000/login/admin/{}/{}'.format(userId,email))
        else:
         return render(request,'authentication/admin_buses_details.html',data)
           

    elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
    else:
        return render(request,'authentication/error.html') 

def Admin_Buses_Schedule(request,userId,email):
 if request.session.get('email')== email and request.session.get('role')=='admin':
     date_filter = request.GET.get('date_from')
     cursor = connection.cursor()
     if date_filter==None:
         cursor.execute("""SELECT * FROM bus_schedule""")
     else:
         print(date_filter)
         print(date_filter)
         cursor.execute("""SELECT * FROM bus_schedule WHERE date_from=%s""",[date_filter])
     row = cursor.fetchall()
     schedules=[]
     a = cursor.rowcount
     if a!=0:
         for n in range(a):
          schedules.append({
            'bus_no':row[n][0],
            'date_from':row[n][1],
            'date_to':row[n][2],
            'seats':row[n][4]
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
         cursor.execute("""SELECT Time_From,seat_Capacity FROM bus_details JOIN bus_schedule ON bus_details.Bus_No = bus_schedule.Bus_No JOIN bus ON bus.Bus_ID = bus_details.Bus_ID WHERE bus_details.Bus_No =%s""",[bus_no])
         if cursor.rowcount==0:
             messages.success(request,'bus with the entered bus number does not exist, please add the bus no in the bus details first!!')
             return redirect('http://127.0.0.1:8000/login/admin/{}/{}/buses/details'.format(userId,email))
         else:
             now = datetime.now()
             now = now.strftime("%Y-%m-%d %H:%M:%S")
             time_from_db = row[0][1].strftime("%H:%M:%S")
             date_time_db = date_from+' '+time_from_db
             if date_time_db<now:
                 messages.success(request,'you cannot add a bus schedule in the past')
                 return redirect('http://127.0.0.1:8000/login/admin/{}/{}/buses/schedule'.format(userId,email))
             else:
               row = cursor.fetchall()
               seats=row[0][1]
               cursor.execute("""SELECT * FROM bus_schedule""")
               count = cursor.rowcount
               count = count +1
               cursor.execute("""INSERT INTO bus_schedule (Bus_No,date_from,date_to,no_of_seats_vacant,Total_seats) VALUES(%s,%s,%s,%s,%s)""",(bus_no,date_from,date_to,int(seats),int(seats),))
               messages.success(request,'bus schedule added successfully')
               return redirect('http://127.0.0.1:8000/login/admin/{}/{}'.format(userId,email))
     else:
         return render(request,'authentication/admin_buses_schedule.html',data)
 elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
 else:
        return render(request,'authentication/error.html')
