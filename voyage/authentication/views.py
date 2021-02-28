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

def sortFunc(e):
    return e['seat_no']

#  views starts here

def Flights(request):
 userId=request.session.get('userId')
 email=request.session.get('email')
 if  request.session.get('role')=='user':
    if request.method == "POST":
        from_p = request.POST.get("startfrom")
        to_p = request.POST.get("destination")
        date = request.POST.get("dateOfTravel")
        passengers = request.POST.get("travellers")
        return redirect('/flights/search/?startfrom={}&destination={}&dateOfTravel={}&travellers={}'.format(from_p, to_p, date, passengers))

    else:

        cursor = connection.cursor()
        cursor.execute("""SELECT firstname,lastname,wallet FROM users WHERE userID=%s""", [userId])
        row = cursor.fetchall()
        firstname = row[0][0]
        lastname = row[0][1]
        wallet = row[0][2]

        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT from_p FROM route")
        a = cursor.rowcount
        row = cursor.fetchall()
        from_p_list = []
        for n in range(a):
            from_p_list.append(row[n][0])

        cursor.execute("SELECT DISTINCT to_p FROM route")
        a = cursor.rowcount
        row = cursor.fetchall()
        to_p_list = []
        for n in range(a):
            to_p_list.append(row[n][0])
        data = {
            'userId': userId,
            'email': email,
            'firstname': firstname,
            'lastname': lastname,
            'wallet': wallet,
            'from_p_list': from_p_list,
            'to_p_list': to_p_list
        }
        return render(request, 'authentication/flights.html', data)
 elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
 else:
        return render(request,'authentication/error.html')


def Flights_Search(request):
 userId=request.session.get('userId')
 email=request.session.get('email')   
 if  request.session.get('role')=='user':
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT from_p FROM route")
    a = cursor.rowcount
    row = cursor.fetchall()
    from_p_list = []
    for n in range(a):
        from_p_list.append(row[n][0])

    cursor.execute("SELECT DISTINCT to_p FROM route")
    a = cursor.rowcount
    row = cursor.fetchall()
    to_p_list = []
    for n in range(a):
        to_p_list.append(row[n][0])

    cursor.execute(
        """SELECT firstname,lastname,wallet FROM users WHERE userID=%s""", [userId])
    row = cursor.fetchall()
    firstname = row[0][0]
    lastname = row[0][1]
    wallet = row[0][2]
    from_p = request.GET.get('startfrom')
    to_p = request.GET.get('destination')
    date = request.GET.get('dateOfTravel')
    passengers = int(request.GET.get('travellers'))
    if request.method == "POST":
        from_p = request.GET.get('startfrom')
        to_p = request.GET.get('destination')
        date = request.GET.get('dateOfTravel')
        passengers = int(request.GET.get('travellers'))
        minm_price = int(request.POST.get("minm_price"))
        maxm_price = int(request.POST.get("maxm_price"))
        cursor = connection.cursor()
        cursor.execute("""select FSID,Company,from_p,to_p,Time_From,Time_To,Price,no_of_seats_vacant
             FROM flight_schedule JOIN flight_details ON flight_schedule.Flight_No=flight_details.Flight_No JOIN route ON route.RID=flight_details.RID JOIN flight ON flight.Flight_ID=flight_details.Flight_ID
             WHERE no_of_seats_vacant>0 AND date_from=%s AND from_p=%s AND to_p=%s AND Price BETWEEN %s AND %s """, (date, from_p, to_p, minm_price, maxm_price))
        a = cursor.rowcount
        row = cursor.fetchall()
        if cursor.rowcount != 0:
            flights = []
            for n in range(a):
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                date_time = date+' '+row[n][4].strftime("%H:%M")
                if date_time>now:
                 flights.append({
                    'flight_schedule': row[n][0],
                    'company': row[n][1],
                    'from_p': row[n][2],
                    'to_p': row[n][3],
                    'time_from': row[n][4].strftime("%H:%M"),
                    'time_to': row[n][5].strftime("%H:%M"),
                    'price': row[n][6],
                    'available': row[n][7],
                    'image':'fa fa-plane fa-3x'
                 })

                data = {
                    'userId': userId,
                    'firstname': firstname,
                    'lastname': lastname,
                    'wallet': wallet,
                    'email': email,
                    'from_p': from_p,
                    'to_p': to_p,
                    'date': date,
                    'passengers': passengers,
                    'flights': flights,
                    'from_p_list': from_p_list,
                    'to_p_list': to_p_list,
                    'minm_price': minm_price,
                    'maxm_price': maxm_price,
                }
            return render(request, 'authentication/flights_search.html', data)
        else:
            data = {
                'userId': userId,
                'firstname': firstname,
                'lastname': lastname,
                'wallet': wallet,
                'email': email,
                'from_p': from_p,
                'to_p': to_p,
                'date': date,
                'flights': None,
                'passengers': passengers,
                'from_p_list': from_p_list,
                'to_p_list': to_p_list,
                'minm_price': minm_price,
                'maxm_price': maxm_price,
            }
            return render(request, 'authentication/flights_search.html', data)
    else:
        cursor = connection.cursor()
        cursor.execute("""select FSID,Company,from_p,to_p,Time_From,Time_To,Price,no_of_seats_vacant
        FROM flight_schedule JOIN flight_details ON flight_schedule.Flight_No=flight_details.Flight_No JOIN route ON route.RID=flight_details.RID JOIN flight ON flight.Flight_ID=flight_details.Flight_ID
        WHERE no_of_seats_vacant>0 AND date_from=%s AND from_p=%s AND to_p=%s""", (date, from_p, to_p))
        a = cursor.rowcount
        row = cursor.fetchall()
        if cursor.rowcount != 0:
            flights = []
            for n in range(a):
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                date_time = date+' '+row[n][4].strftime("%H:%M")
                if date_time>now:
                 flights.append({
                    'flight_schedule': row[n][0],
                    'company': row[n][1],
                    'from_p': row[n][2],
                    'to_p': row[n][3],
                    'time_from': row[n][4].strftime("%H:%M"),
                    'time_to': row[n][5].strftime("%H:%M"),
                    'price': row[n][6],
                    'available': row[n][7],
                    'image':'fa fa-plane fa-3x'
                 })
                data = {
                    'userId': userId,
                    'firstname': firstname,
                    'lastname': lastname,
                    'wallet': wallet,
                    'email': email,
                    'from_p': from_p,
                    'to_p': to_p,
                    'date': date,
                    'passengers': passengers,
                    'flights': flights,
                    'from_p_list': from_p_list,
                    'to_p_list': to_p_list,
                }
            return render(request, 'authentication/flights_search.html', data)
        else:
            data = {
                'userId': userId,
                'firstname': firstname,
                'lastname': lastname,
                'wallet': wallet,
                'email': email,
                'from_p': from_p,
                'to_p': to_p,
                'date': date,
                'flights': None,
                'passengers': passengers,
                'from_p_list': from_p_list,
                'to_p_list': to_p_list
            }
            return render(request, 'authentication/flights_search.html', data)
 elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
 else:
        return render(request,'authentication/error.html')


def Flights_Book(request):
 userId=request.session.get('userId')
 email=request.session.get('email')
 if  request.session.get('role')=='user':
   if request.method == "POST":
      flight_schedule=request.GET.get("c1")
      flight_schedule=int(flight_schedule)
      passengers=(request.GET.get("c2"))
      passengers=int(passengers)
      cursor = connection.cursor()
      cursor.execute("""SELECT wallet FROM users WHERE userID=%s""", [userId])
      row = cursor.fetchall()
      wallet = row[0][0]
      cursor = connection.cursor()
      cursor.execute("""SELECT Price,from_p,to_p,date_from FROM flight_schedule JOIN flight_details ON flight_schedule.Flight_No=flight_details.Flight_No JOIN route ON flight_details.RID=route.RID WHERE FSID=%s""", [flight_schedule])
      row = cursor.fetchall()
      total_fare = (row[0][0])*passengers
      from_p = row[0][1]
      to_p = row[0][2]
      date_from = row[0][3]

      if wallet>=total_fare:
         wallet = wallet-total_fare
         cursor = connection.cursor()
         cursor.execute("""UPDATE users SET wallet=%s WHERE userID=%s""", (wallet, userId))
         cursor = connection.cursor()
         now=datetime.now()
         date_time=now.strftime("%Y-%m-%d %H:%M:%S")
         cursor.execute("""INSERT INTO flight_ticket(User_ID,Date_of_booking,FSID,No_of_passengers,status,amount) VALUES(%s,%s,%s,%s,%s,%s)""",(userId,date_time,flight_schedule,passengers,'booked',total_fare))
         cursor = connection.cursor()
         cursor.execute("""SELECT Booking_ID FROM flight_ticket WHERE User_ID=%s and Date_of_booking=%s""", (userId,date_time))
         row = cursor.fetchall()
         booking_id = row[0][0]
         subject = 'E-ticket for booking id:{}'.format(row[0][0])
         text_content = 'You are receiving this message because your booking is confirmed with the booking id:{} the booking details  can be viewed through the website in the my bookings section we hope u have a great journey!!'.format(row[0][0])
         cursor = connection.cursor()
         cursor.execute("""INSERT INTO flight_transaction(booking_ID,description,amount) VALUES(%s,%s,%s)""",(booking_id,"payment",total_fare))
         cursor = connection.cursor()
         cursor.execute("""SELECT no_of_seats_vacant,seat_Capacity FROM flight_schedule JOIN flight_details ON flight_schedule.Flight_No=flight_details.Flight_No JOIN flight ON flight_details.Flight_ID=flight.Flight_ID WHERE FSID=%s""", [flight_schedule])
         row = cursor.fetchall()
         vacant = row[0][0]
         total = row[0][1]
         cursor=connection.cursor()
         cursor.execute("""SELECT Seat_no FROM flight_schedule JOIN flight_ticket ON flight_schedule.FSID=flight_ticket.FSID JOIN flight_passenger ON flight_ticket.Booking_ID=flight_passenger.Booking_ID WHERE flight_schedule.FSID=%s and status=%s""",(flight_schedule,"booked"))
         row=cursor.fetchall()
         booked=[]
         if cursor.rowcount!=0:
             for k in range(cursor.rowcount):
                 booked.append(row[k][0])
         cursor=connection.cursor()
         cursor.execute("""SELECT DISTINCT Seat_no FROM flight_schedule JOIN flight_ticket ON flight_schedule.FSID=flight_ticket.FSID JOIN flight_passenger ON flight_ticket.Booking_ID=flight_passenger.Booking_ID WHERE flight_schedule.FSID=%s and status=%s""",(flight_schedule,"cancelled"))
         row=cursor.fetchall()
         cancelled=[]
         if cursor.rowcount!=0:
            for m in range(cursor.rowcount):
                print(row[m][0])
                cancelled.append(row[m][0])
         common=[]
         if len(booked)!=0:
             for p in range(len(cancelled)):
                 if cancelled[p] in booked:
                     common.append(cancelled[p])
         if len(common)!=0:
             for q in range(len(common)):
                 cancelled.remove(common[q])
         for n in range(1,passengers+1):
            name = request.POST.get('name{}'.format(n))
            age = request.POST.get('age{}'.format(n))
            gender = request.POST.get('gender{}'.format(n))
            if len(cancelled)!=0:
                seat=cancelled.pop()
            else:
                seat=total-vacant+n
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO flight_passenger(Name,Gender,Age,Booking_ID,Seat_no) VALUES(%s,%s,%s,%s,%s)""",(name, gender, age, booking_id, seat))
         no_of_seats_vacant = vacant-passengers
         cursor = connection.cursor()
         cursor.execute("""UPDATE flight_schedule SET no_of_seats_vacant=%s WHERE FSID=%s""",(no_of_seats_vacant,flight_schedule))
         msg = EmailMultiAlternatives(subject, text_content, 'cse190001033@iiti.ac.in', [email])
         msg.send()
         messages.success(request,"Booking Successful!Check Your Ticket In My Bookings")
         return redirect("/home")
      else:
          messages.success(request,"No Sufficient Money For Transaction In Wallet!")
          return redirect("/flights/search/?startfrom={}&destination={}&dateOfTravel={}&travellers={}".format(from_p, to_p,date_from,passengers))
   else:
      flight_schedule=request.GET.get("c1")
      flight_schedule=int(flight_schedule)
      passengers=(request.GET.get("c2"))
      passengers=int(passengers)
      cursor=connection.cursor()
      cursor.execute("""SELECT firstname,lastname,wallet FROM users WHERE userID=%s""", [userId])
      row=cursor.fetchall()
      firstname=row[0][0]
      lastname=row[0][1]
      wallet=row[0][2]
      cursor=connection.cursor()
      cursor.execute("""SELECT Company,from_p,to_p,Time_From,Time_To,Price,no_of_seats_vacant,date_from FROM flight_schedule JOIN flight_details ON flight_schedule.Flight_No=flight_details.Flight_No JOIN route ON route.RID=flight_details.RID JOIN flight ON flight.Flight_ID=flight_details.Flight_ID WHERE FSID=%s""", [flight_schedule])
      row=cursor.fetchall()
      company=row[0][0]
      from_p=row[0][1]
      to_p=row[0][2]
      time_from=row[0][3].strftime("%H:%M")
      time_to=row[0][4].strftime("%H:%M")
      price=row[0][5]
      available=row[0][6]
      date_from=row[0][7]
      data={
            'userId': userId,
            'email': email,
            'firstname': firstname,
            'lastname': lastname,
            'wallet': wallet,
            'company': company,
            'from_p': from_p,
            'to_p': to_p,
            'time_from': time_from,
            'time_to': time_to,
            'price': price,
            'available': available,
            'no_of_passengers': passengers,
            'total_fare': passengers*price,
            'passengers': range(1, passengers+1),
            'flight_schedule': flight_schedule,
            'image':"fa fa-plane fa-3x"
        }
      if passengers>0:
          if passengers<=available:
              return render(request, 'authentication/flights_book.html', data)
          else:
              messages.success(request, 'No.of passengers excede available no.of seats!')
              return redirect('/flights/search/?startfrom={}&destination={}&dateOfTravel={}&travellers={}'.format(from_p, to_p, date_from, passengers))
      else:
          messages.success(request, 'please select valid number of passengers!')
          return redirect('/flights/search/?startfrom={}&destination={}&dateOfTravel={}&travellers={}'.format(from_p, to_p, date_from, passengers))
 elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
 else:
        return render(request,'authentication/error.html')

#flights views ends here buses part starts here.

def Buses(request):
 userId=request.session.get('userId')
 email=request.session.get('email')
 if  request.session.get('role')=='user':
    if request.method == "POST":
        from_p = request.POST.get("startfrom")
        to_p = request.POST.get("destination")
        date = request.POST.get("dateOfTravel")
        passengers = request.POST.get("travellers")
        return redirect('/buses/search/?startfrom={}&destination={}&dateOfTravel={}&travellers={}'.format(from_p, to_p, date, passengers))

    else:

        cursor = connection.cursor()
        cursor.execute(
            """SELECT firstname,lastname,wallet FROM users WHERE userID=%s""", [userId])
        row = cursor.fetchall()
        firstname = row[0][0]
        lastname = row[0][1]
        wallet = row[0][2]

        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT from_p FROM route")
        a = cursor.rowcount
        row = cursor.fetchall()
        from_p_list = []
        for n in range(a):
            from_p_list.append(row[n][0])

        cursor.execute("SELECT DISTINCT to_p FROM route")
        a = cursor.rowcount
        row = cursor.fetchall()
        to_p_list = []
        for n in range(a):
            to_p_list.append(row[n][0])
        data = {
            'userId': userId,
            'email': email,
            'firstname': firstname,
            'lastname': lastname,
            'wallet': wallet,
            'from_p_list': from_p_list,
            'to_p_list': to_p_list
        }
        return render(request, 'authentication/buses.html', data)
 elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
 else:
        return render(request,'authentication/error.html')


def Buses_Search(request):
 userId=request.session.get('userId')
 email=request.session.get('email')
 if  request.session.get('role')=='user':
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT from_p FROM route")
    a = cursor.rowcount
    row = cursor.fetchall()
    from_p_list = []
    for n in range(a):
        from_p_list.append(row[n][0])

    cursor.execute("SELECT DISTINCT to_p FROM route")
    a = cursor.rowcount
    row = cursor.fetchall()
    to_p_list = []
    for n in range(a):
        to_p_list.append(row[n][0])

    cursor.execute(
        """SELECT firstname,lastname,wallet FROM users WHERE userID=%s""", [userId])
    row = cursor.fetchall()
    firstname = row[0][0]
    lastname = row[0][1]
    wallet = row[0][2]

    from_p = request.GET.get('startfrom')
    to_p = request.GET.get('destination')
    date = request.GET.get('dateOfTravel')
    passengers = int(request.GET.get('travellers'))
    if request.method == "POST":
        from_p = request.GET.get('startfrom')
        to_p = request.GET.get('destination')
        date = request.GET.get('dateOfTravel')  
        passengers = int(request.GET.get('travellers'))
        minm_price = int(request.POST.get("minm_price"))
        maxm_price = int(request.POST.get("maxm_price"))
        cursor = connection.cursor()  
        cursor.execute("""select BSID,Company,from_p,to_p,Time_From,Time_To,Price,no_of_seats_vacant
        FROM bus_schedule JOIN bus_details ON bus_schedule.Bus_No=bus_details.Bus_No JOIN route ON route.RID=bus_details.RID JOIN bus ON bus.Bus_ID=bus_details.Bus_ID
        WHERE no_of_seats_vacant>0 AND date_from=%s AND from_p=%s AND to_p=%s AND Price BETWEEN %s AND %s """, (date, from_p, to_p, minm_price, maxm_price))
        a = cursor.rowcount
        row = cursor.fetchall()
        if cursor.rowcount != 0:
            buses = []
            for n in range(a):
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                date_time = date+' '+row[n][4].strftime("%H:%M")
                if date_time>now:
                 buses.append({
                    'bus_schedule': row[n][0],
                    'company': row[n][1],
                    'from_p': row[n][2],
                    'to_p': row[n][3],
                    'time_from': row[n][4].strftime("%H:%M"),
                    'time_to': row[n][5].strftime("%H:%M"),
                    'price': row[n][6],
                    'available': row[n][7],
                    'image': 'fa fa-bus fa-3x'
                 })

                data = {
                    'userId': userId,
                    'firstname': firstname,
                    'lastname': lastname,
                    'wallet': wallet,
                    'email': email,
                    'from_p': from_p,
                    'to_p': to_p,
                    'date': date,
                    'passengers': passengers,
                    'buses': buses,
                    'from_p_list': from_p_list,
                    'to_p_list': to_p_list,
                    'minm_price': minm_price,
                    'maxm_price': maxm_price,
                }
            return render(request, 'authentication/buses_search.html', data)
        else:
            data = {
                'userId': userId,
                'firstname': firstname,
                'lastname': lastname,
                'wallet': wallet,
                'email': email,
                'from_p': from_p,
                'to_p': to_p,
                'date': date,
                'buses': None,
                'passengers': passengers,
                'from_p_list': from_p_list,
                'to_p_list': to_p_list,
                'minm_price': minm_price,
                'maxm_price': maxm_price,

            }
            return render(request, 'authentication/buses_search.html', data)
    else:
        cursor = connection.cursor()
        cursor.execute("""select BSID,Company,from_p,to_p,Time_From,Time_To,Price,no_of_seats_vacant
        FROM bus_schedule JOIN bus_details ON bus_schedule.Bus_No=bus_details.Bus_No JOIN route ON route.RID=bus_details.RID JOIN bus ON bus.Bus_ID=bus_details.Bus_ID
        WHERE no_of_seats_vacant>0 AND date_from=%s AND from_p=%s AND to_p=%s""", (date, from_p, to_p))
        a = cursor.rowcount
        row = cursor.fetchall()
        if cursor.rowcount != 0:
            buses = []
            for n in range(a):
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                date_time = date+' '+row[n][4].strftime("%H:%M")
                if date_time>now:
                 buses.append({
                    'bus_schedule': row[n][0],
                    'company': row[n][1],
                    'from_p': row[n][2],
                    'to_p': row[n][3],
                    'time_from': row[n][4].strftime("%H:%M"),
                    'time_to': row[n][5].strftime("%H:%M"),
                    'price': row[n][6],
                    'available': row[n][7],
                    'image':'fa fa-bus fa-3x'
                 })
                data = {
                    'userId': userId,
                    'firstname': firstname,
                    'lastname': lastname,
                    'wallet': wallet,
                    'email': email,
                    'from_p': from_p,
                    'to_p': to_p,
                    'date': date,
                    'passengers': passengers,
                    'buses': buses,
                    'from_p_list': from_p_list,
                    'to_p_list': to_p_list,
                }
            return render(request, 'authentication/buses_search.html', data)
        else:
            data = {
                'userId': userId,
                'firstname': firstname,
                'lastname': lastname,
                'wallet': wallet,
                'email': email,
                'from_p': from_p,
                'to_p': to_p,
                'date': date,
                'buses': None,
                'passengers': passengers,
                'from_p_list': from_p_list,
                'to_p_list': to_p_list
            }
            return render(request, 'authentication/buses_search.html', data)
 elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
 else:
        return render(request,'authentication/error.html')




def Buses_Book(request):
 userId=request.session.get('userId')
 email=request.session.get('email')
 if  request.session.get('role')=='user':
   if request.method == "POST":
      bus_schedule=request.GET.get("c1")
      bus_schedule=int(bus_schedule)
      passengers=(request.GET.get("c2"))
      passengers=int(passengers)
      cursor = connection.cursor()
      cursor.execute("""SELECT wallet FROM users WHERE userID=%s""", [userId])
      row = cursor.fetchall()
      wallet = row[0][0]
      cursor = connection.cursor()
      cursor.execute("""SELECT Price,from_p,to_p,date_from FROM bus_schedule JOIN bus_details ON bus_schedule.Bus_No=bus_details.Bus_No JOIN route ON bus_details.RID=route.RID WHERE BSID=%s""", [bus_schedule])
      row = cursor.fetchall()
      total_fare = (row[0][0])*passengers
      from_p = row[0][1]
      to_p = row[0][2]
      date_from = row[0][3]

      if wallet>=total_fare:
         wallet = wallet-total_fare
         cursor = connection.cursor()
         cursor.execute("""UPDATE users SET wallet=%s WHERE userID=%s""", (wallet, userId))
         cursor = connection.cursor()
         now=datetime.now()
         date_time=now.strftime("%Y-%m-%d %H:%M:%S")
         cursor.execute("""INSERT INTO bus_ticket(User_ID,Date_of_booking,BSID,No_of_passengers,status,amount) VALUES(%s,%s,%s,%s,%s,%s)""",(userId,date_time,bus_schedule,passengers,'booked',total_fare))
         cursor = connection.cursor()
         cursor.execute("""SELECT Booking_ID FROM bus_ticket WHERE User_ID=%s and Date_of_booking=%s""", (userId,date_time))
         row = cursor.fetchall()
         
         booking_id = row[0][0]
         subject = 'E-ticket for booking id:{}'.format(row[0][0])
         text_content = 'You are receiving this message because your booking is confirmed with the booking id:{} the booking details  can be viewed through the website in the my bookings section we hope u have a great journey!!'.format(row[0][0])
         cursor = connection.cursor()
         cursor.execute("""INSERT INTO bus_transaction(booking_ID,description,amount) VALUES(%s,%s,%s)""",(booking_id,"payment",total_fare))
         cursor = connection.cursor()
         cursor.execute("""SELECT no_of_seats_vacant,seat_Capacity FROM bus_schedule JOIN bus_details ON bus_schedule.Bus_No=bus_details.Bus_No JOIN bus ON bus_details.Bus_ID=bus.Bus_ID WHERE BSID=%s""", [bus_schedule])
         row = cursor.fetchall()
         vacant = row[0][0]
         total = row[0][1]
         cursor = connection.cursor()
         cursor.execute("""SELECT Seat_no FROM bus_schedule JOIN bus_ticket ON bus_schedule.BSID=bus_ticket.BSID JOIN bus_passenger ON bus_ticket.Booking_ID=bus_passenger.Booking_ID WHERE bus_schedule.BSID=%s and status=%s""",(bus_schedule,"booked"))
         row=cursor.fetchall()
         booked=[]
         if cursor.rowcount!=0:
             for n in range(cursor.rowcount):
                 booked.append(row[n][0])
         cursor = connection.cursor()
         cursor.execute("""SELECT DISTINCT Seat_no FROM bus_schedule JOIN bus_ticket ON bus_schedule.BSID=bus_ticket.BSID JOIN bus_passenger ON bus_ticket.Booking_ID=bus_passenger.Booking_ID WHERE bus_schedule.BSID=%s and status=%s""",(bus_schedule,"cancelled"))
         row=cursor.fetchall()
         cancelled=[]
         if cursor.rowcount!=0:
             for m in range(cursor.rowcount):
                 cancelled.append(row[m][0])
         common=[]
         if len(booked)!=0:
             for p in range(len(cancelled)):
                 if cancelled[p] in booked:
                     common.append(cancelled[p])
         if len(common)!=0:
             for q in range(len(common)):
                 cancelled.remove(common[q])
         print(cancelled)
         for n in range(1,passengers+1):
            name = request.POST.get('name{}'.format(n))
            age = request.POST.get('age{}'.format(n))
            gender = request.POST.get('gender{}'.format(n))
            if len(cancelled)!=0:
                seat=cancelled.pop()
            else:
                seat = total-vacant+n
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO bus_passenger(Name,Gender,Age,Booking_ID,Seat_no) VALUES(%s,%s,%s,%s,%s)""",(name, gender, age, booking_id, seat))
         no_of_seats_vacant = vacant-passengers
         cursor = connection.cursor()
         cursor.execute("""UPDATE bus_schedule SET no_of_seats_vacant=%s WHERE BSID=%s""",(no_of_seats_vacant,bus_schedule))
         messages.success(request,"Booking Successful!Check Your Ticket In My Bookings")
         msg = EmailMultiAlternatives(subject, text_content, 'cse190001033@iiti.ac.in', [email],)
         msg.send()
         return redirect("/home")
      else:
          messages.success(request,"No Sufficient Money For Transaction In Wallet!")
          return redirect("/buses/search/?startfrom={}&destination={}&dateOfTravel={}&travellers={}".format(from_p, to_p,date_from,passengers))
   else:
      bus_schedule=request.GET.get("c1")
      bus_schedule=int(bus_schedule)
      passengers=(request.GET.get("c2"))
      passengers=int(passengers)
      cursor=connection.cursor()
      cursor.execute("""SELECT firstname,lastname,wallet FROM users WHERE userID=%s""", [userId])
      row=cursor.fetchall()
      firstname=row[0][0]
      lastname=row[0][1]
      wallet=row[0][2]
      cursor=connection.cursor()
      cursor.execute("""SELECT Company,from_p,to_p,Time_From,Time_To,Price,no_of_seats_vacant,date_from FROM bus_schedule JOIN bus_details ON bus_schedule.Bus_No=bus_details.Bus_No JOIN route ON route.RID=bus_details.RID JOIN bus ON bus.Bus_ID=bus_details.Bus_ID WHERE BSID=%s""", [bus_schedule])
      row=cursor.fetchall()
      company=row[0][0]
      from_p=row[0][1]
      to_p=row[0][2]
      time_from=row[0][3].strftime("%H:%M")
      time_to=row[0][4].strftime("%H:%M")
      price=row[0][5]
      available=row[0][6]
      date_from=row[0][7]
      data={
            'userId': userId,
            'email': email,
            'firstname': firstname,
            'lastname': lastname,
            'wallet': wallet,
            'company': company,
            'from_p': from_p,
            'to_p': to_p,
            'time_from': time_from,
            'time_to': time_to,
            'price': price,
            'available': available,
            'no_of_passengers': passengers,
            'total_fare': passengers*price,
            'passengers': range(1, passengers+1),
            'bus_schedule': bus_schedule,
            'image':'fa fa-bus fa-3x'
        }
      if passengers>0:
          if passengers<=available:
              return render(request, 'authentication/buses_book.html', data)
          else:
              messages.success(request, 'No.of passengers excede available no.of seats!')
              return redirect('/buses/search/?startfrom={}&destination={}&dateOfTravel={}&travellers={}'.format(from_p, to_p, date_from, passengers))
      else:
          messages.success(request, 'please select valid number of passengers!')
          return redirect('/buses/search/?startfrom={}&destination={}&dateOfTravel={}&travellers={}'.format(from_p, to_p, date_from, passengers))
 elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
 else:
        return render(request,'authentication/error.html')



#buses views ends here boking views starts here.

def My_Bookings(request):
 userId=request.session.get('userId')
 email=request.session.get('email')
 if  request.session.get('role')=='user':
    cursor = connection.cursor()
    cursor.execute("""SELECT firstname,lastname,wallet FROM users WHERE userID=%s""", [userId])
    user = cursor.fetchall()
    firstname = user[0][0]
    lastname = user[0][1]
    wallet = user[0][2]
    cursor.execute("""SELECT Booking_ID,Date_of_booking,No_of_passengers,Price,Company,Time_From,Time_To,from_p,to_p,status,date_from,date_to
    FROM bus_ticket JOIN users ON bus_ticket.User_ID=users.userID JOIN bus_schedule ON bus_ticket.BSID=bus_schedule.BSID JOIN bus_details ON bus_details.Bus_No=bus_schedule.Bus_No JOIN bus ON bus_details.Bus_ID=Bus.Bus_ID
    JOIN route ON route.RID=bus_details.RID WHERE userID=%s ORDER BY Date_of_booking DESC""",[userId])
    row = cursor.fetchall()
    a = cursor.rowcount
    bus_bookings = []
    for n in range(a):
        bus_bookings.append({
             'booking_id':row[n][0],
                'date_of_booking':row[n][1],
                'no_of_passengers':row[n][2],
                'price_per_person':row[n][3],
                'total_price':row[n][3]*row[n][2],
                'company':row[n][4],
                'time_from':row[n][5].strftime("%H:%M"),
                'time_to':row[n][6].strftime("%H:%M"),
                'from_p':row[n][7],
                'to_p':row[n][8],
                'status':row[n][9],
                'date_from':row[n][10],
                'date_to':row[n][11],
                'image':'fa fa-bus fa-3x',
                'type':'bus'
        })

    cursor.execute("""SELECT Booking_ID,Date_of_booking,No_of_passengers,Price,Company,Time_From,Time_To,from_p,to_p,status,date_from,date_to
    FROM flight_ticket JOIN users ON flight_ticket.User_ID=users.userID JOIN flight_schedule ON flight_ticket.FSID=flight_schedule.FSID JOIN flight_details ON flight_details.Flight_No=flight_schedule.Flight_No JOIN flight ON flight_details.Flight_ID=flight.Flight_ID
    JOIN route ON route.RID=flight_details.RID WHERE userID=%s ORDER BY Date_of_booking DESC""",[userId])
    row = cursor.fetchall()
    a = cursor.rowcount
   
    flight_bookings = []
    for n in range(a):
        flight_bookings.append({
                'booking_id':row[n][0],
                'date_of_booking':row[n][1],
                'no_of_passengers':row[n][2],
                'price_per_person':row[n][3],
                'total_price':row[n][3]*row[n][2],
                'company':row[n][4],
                'time_from':row[n][5].strftime("%H:%M"),
                'time_to':row[n][6].strftime("%H:%M"),
                'from_p':row[n][7],
                'to_p':row[n][8],
                'status':row[n][9],
                'date_from':row[n][10],
                'date_to':row[n][11],
                'image':'fa fa-plane fa-3x',
                'type':'flight'
            })
    bookings = []
    bookings = bus_bookings+flight_bookings
    
    if len(bookings)!=0:
        bookings.sort(reverse = True,key=myFunc)
        data={
            'bookings':bookings,
            'userId':userId,
            'email':email,
            'firstname':firstname,
            'lastname':lastname,
            'wallet':wallet

        }

        return render(request,'authentication/my_bookings.html',data)
    else:
        data={
            'bookings':None,
            'userId':userId,
            'email':email,
            'firstname':firstname,
            'lastname':lastname,
            'wallet':wallet
        }
        return render(request,'authentication/my_bookings.html',data)
 elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
 else:
        return render(request,'authentication/error.html')
# Create your views here.


def Booking_Details(request,type_of_transport,bookingId):
 userId=request.session.get('userId')
 email=request.session.get('email')
 if  request.session.get('role')=='user':
    if request.method=="POST":
        if type_of_transport=='flight':
            cursor = connection.cursor()
            cursor.execute("""SELECT No_of_passengers,Price,flight_ticket.FSID,no_of_seats_vacant,date_from,Time_From FROM  flight_ticket JOIN flight_schedule ON flight_ticket.FSID=flight_schedule.FSID JOIN flight_details ON flight_schedule.Flight_No=flight_details.Flight_No WHERE Booking_ID=%s""", [bookingId])
            row=cursor.fetchall()
            no_of_passengers=row[0][0]
            price=row[0][1]
            fsid=row[0][2]
            no_of_seats_vacant=row[0][3]
            date_from=row[0][4]
            time_from=row[0][5]
            date_from=date_from.strftime("%Y-%m-%d")
            time_from=time_from.strftime("%H:%M:%S")
            date_time=date_from+" "+time_from
            now=datetime.now()
            Date_Time=now.strftime("%Y-%m-%d %H:%M:%S")
            if Date_Time<date_time:
                no_of_seats_vacant=no_of_seats_vacant+no_of_passengers
                cursor = connection.cursor()
                cursor.execute("""UPDATE flight_schedule SET no_of_seats_vacant=%s WHERE FSID=%s""",(no_of_seats_vacant,fsid))
                cursor = connection.cursor()
                cursor.execute("""UPDATE flight_ticket SET status=%s WHERE Booking_ID=%s""",("Cancelled",bookingId))
                cursor = connection.cursor()
                cursor.execute("""SELECT wallet FROM users WHERE userID=%s""",[userId])
                row=cursor.fetchall()
                wallet=row[0][0]
                wallet=wallet + (price*no_of_passengers)
                cursor = connection.cursor()
                cursor.execute("""UPDATE users SET wallet=%s WHERE userID=%s""",(wallet,userId))
                cursor = connection.cursor()
                cursor.execute("""INSERT INTO flight_transaction(booking_ID,description,amount) VALUES(%s,%s,%s)""",(bookingId,"refund",(price*no_of_passengers)))
                messages.success(request, 'Ticket Cancelled Successfully!')
                return redirect("/home")
            else:
                messages.success(request, 'Ticket Cannot Be Cancelled!') 
                return redirect("/mybookings/{}/{}/details".format(type_of_transport,bookingId))
        else:
            cursor = connection.cursor()
            cursor.execute("""SELECT No_of_passengers,Price,bus_ticket.BSID,no_of_seats_vacant,date_from,Time_From FROM  bus_ticket JOIN bus_schedule ON bus_ticket.BSID=bus_schedule.BSID JOIN bus_details ON bus_schedule.Bus_No=bus_details.Bus_No WHERE Booking_ID=%s""", [bookingId])
            row=cursor.fetchall()
            no_of_passengers=row[0][0]
            price=row[0][1]
            bsid=row[0][2]
            no_of_seats_vacant=row[0][3]
            date_from=row[0][4]
            time_from=row[0][5]
            date_from=date_from.strftime("%Y-%m-%d")
            time_from=time_from.strftime("%H:%M:%S")
            date_time=date_from+" "+time_from
            now=datetime.now()
            Date_Time=now.strftime("%Y-%m-%d %H:%M:%S")
            if Date_Time<date_time:
                no_of_seats_vacant=no_of_seats_vacant+no_of_passengers
                cursor = connection.cursor()
                cursor.execute("""UPDATE bus_schedule SET no_of_seats_vacant=%s WHERE BSID=%s""",(no_of_seats_vacant,bsid))
                cursor = connection.cursor()
                cursor.execute("""UPDATE bus_ticket SET status=%s WHERE Booking_ID=%s""",("Cancelled",bookingId))
                cursor = connection.cursor()
                cursor.execute("""SELECT wallet FROM users WHERE userID=%s""",[userId])
                row=cursor.fetchall()
                wallet=row[0][0]
                wallet=wallet + (price*no_of_passengers)
                cursor = connection.cursor()
                cursor.execute("""UPDATE users SET wallet=%s WHERE userID=%s""",(wallet,userId))
                cursor = connection.cursor()
                cursor.execute("""INSERT INTO bus_transaction(booking_ID,description,amount) VALUES(%s,%s,%s)""",(bookingId,"refund",(price*no_of_passengers)))
                messages.success(request, 'Ticket Cancelled Successfully!')
                return redirect("/home")
            else:
                messages.success(request, 'Ticket Cannot Be Cancelled!')
                return redirect("/mybookings/{}/{}/details".format(type_of_transport,bookingId))      
    else:    
        cursor = connection.cursor()
        cursor.execute("""SELECT firstname,lastname,wallet FROM users WHERE userID=%s""", [userId])
        user = cursor.fetchall()
        firstname = user[0][0]
        lastname = user[0][1]
        wallet = user[0][2]
        if type_of_transport =='flight':
        
            cursor.execute("""SELECT Date_of_booking,No_of_passengers,Price,Company,Time_From,Time_To,from_p,to_p,Name,flight_passenger.Gender,Age,Seat_no,status,date_from,date_to
            FROM flight_ticket JOIN users ON flight_ticket.User_ID=users.userID JOIN flight_schedule ON flight_ticket.FSID=flight_schedule.FSID JOIN flight_details ON flight_details.Flight_No=flight_schedule.Flight_No JOIN flight ON flight_details.Flight_ID=flight.Flight_ID
            JOIN route ON route.RID=flight_details.RID JOIN flight_passenger ON flight_passenger.Booking_ID=flight_ticket.Booking_ID WHERE userID=%s AND flight_ticket.Booking_ID=%s""",(int(userId),int(bookingId)) )
            row = cursor.fetchall()
            a = cursor.rowcount
            no_of_passengers = a
            passengers=[]
            date_from=row[0][13]
            date_from=date_from.strftime("%Y-%m-%d")
            time_from=row[0][4]
            time_from=time_from.strftime("%H:%M")
            date_time=date_from+" "+time_from
            now = datetime.now()
            Date_Time=now.strftime("%Y-%m-%d %H:%M")
            if row[0][12]=="booked" and Date_Time<date_time:
                status_code=1
            else:
                status_code=None
            for n in range(a):
                passengers.append({
            'name':row[n][8],
            'gender':row[n][9],
            'age':row[n][10],
            'seat_no':row[n][11],
            'no':n+1
                })
            data={
        'passengers':passengers,
        'date_of_booking':row[0][0],
        'no_of_passengers':row[0][1],
        'price_per_person':row[0][2],
        'total_price':row[0][2]*row[0][1],
        'company':row[0][3],
        'time_from':row[0][4].strftime("%H:%M"),
        'time_to':row[0][5].strftime("%H:%M"),
        'from_p':row[0][6],
        'to_p':row[0][7],
        'image':'fa fa-plane fa-3x',
        'firstname':firstname,
        'lastname':lastname,
        'wallet':wallet,
        'email':email,
        'userId':userId,
        'status':row[0][12],
        'date_from':row[0][13],
        'date_to':row[0][14],
        'status_code':status_code,
        'type':'flight',
        'booking_Id':bookingId
            }
            return render(request,'authentication/booking_details.html',data)
        elif type_of_transport =='bus':
        
            cursor.execute("""SELECT Date_of_booking,No_of_passengers,Price,Company,Time_From,Time_To,from_p,to_p,Name,bus_passenger.Gender,Age,Seat_no,status,date_from,date_to
            FROM bus_ticket JOIN users ON bus_ticket.User_ID=users.userID JOIN bus_schedule ON bus_ticket.BSID=bus_schedule.BSID JOIN bus_details ON bus_details.Bus_No=bus_schedule.Bus_No JOIN bus ON bus_details.Bus_ID=bus.Bus_ID
            JOIN route ON route.RID=bus_details.RID JOIN bus_passenger ON bus_passenger.Booking_ID=bus_ticket.Booking_ID WHERE userID=%s AND bus_ticket.Booking_ID=%s""",(int(userId),int(bookingId)) )
            row = cursor.fetchall()
            a = cursor.rowcount
            no_of_passengers = a
            passengers=[]
            date_from=row[0][13]
            date_from=date_from.strftime("%Y-%m-%d")
            time_from=row[0][4]
            time_from=time_from.strftime("%H:%M")
            date_time=date_from+" "+time_from
            now = datetime.now()
            Date_Time=now.strftime("%Y-%m-%d %H:%M")
            if row[0][12]=="booked" and Date_Time<date_time:
                status_code=1
            else:
                status_code=None
            for n in range(a):
                passengers.append({
            'name':row[n][8],
            'gender':row[n][9],
            'age':row[n][10],
            'seat_no':row[n][11],
            'no':n+1
                })
            data={
        'passengers':passengers,
        'date_of_booking':row[0][0],
        'no_of_passengers':row[0][1],
        'price_per_person':row[0][2],
        'total_price':row[0][2]*row[0][1],
        'company':row[0][3],
        'time_from':row[0][4].strftime("%H:%M"),
        'time_to':row[0][5].strftime("%H:%M"),
        'from_p':row[0][6],
        'to_p':row[0][7],
        'image':'fa fa-bus fa-3x',
        'firstname':firstname,
        'lastname':lastname,
        'wallet':wallet,
        'email':email,
        'userId':userId,
        'status':row[0][12],
        'date_from':row[0][13],
        'date_to':row[0][14],
        'status_code':status_code,
        'type':'bus',
        'booking_Id':bookingId
            }
            return render(request,'authentication/booking_details.html',data)

 elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
 else:
        return render(request,'authentication/error.html')


def View_ticket_as_PDF(request,type_of_transport,bookingId):
 userId=request.session.get('userId')
 email=request.session.get('email')
 if  request.session.get('role')=='user':
       template_path = 'authentication/{}_pdf.html'.format(type_of_transport)
       cursor = connection.cursor()
       cursor.execute("""SELECT firstname,lastname,wallet FROM users WHERE userID=%s""", [userId])
       user = cursor.fetchall()
       firstname = user[0][0]
       lastname = user[0][1]
       wallet = user[0][2]
       if type_of_transport == 'flight':
        image = 'fa fa-plane fa-3x'
        cursor.execute("""SELECT Date_of_booking,No_of_passengers,Price,Company,Time_From,Time_To,from_p,to_p,Name,flight_passenger.Gender,Age,Seat_no,status,date_from,date_to
        FROM flight_ticket JOIN users ON flight_ticket.User_ID=users.userID JOIN flight_schedule ON flight_ticket.FSID=flight_schedule.FSID JOIN flight_details ON flight_details.Flight_No=flight_schedule.Flight_No JOIN flight ON flight_details.Flight_ID=flight.Flight_ID
        JOIN route ON route.RID=flight_details.RID JOIN flight_passenger ON flight_passenger.Booking_ID=flight_ticket.Booking_ID  WHERE userID=%s AND flight_ticket.Booking_ID=%s""",(int(userId),int(bookingId)))
       elif type_of_transport == 'bus':
        image = 'fa fa-bus fa-3x'
        cursor.execute("""SELECT Date_of_booking,No_of_passengers,Price,Company,Time_From,Time_To,from_p,to_p,Name,bus_passenger.Gender,Age,Seat_no,status,date_from,date_to
        FROM bus_ticket JOIN users ON bus_ticket.User_ID=users.userID JOIN bus_schedule ON bus_ticket.BSID=bus_schedule.BSID JOIN bus_details ON bus_details.Bus_No=bus_schedule.Bus_No JOIN bus ON bus_details.Bus_ID=bus.Bus_ID
        JOIN route ON route.RID=bus_details.RID JOIN bus_passenger ON bus_passenger.Booking_ID=bus_ticket.Booking_ID WHERE userID=%s AND bus_ticket.Booking_ID=%s""",(int(userId),int(bookingId)) )
       row = cursor.fetchall()
       a = cursor.rowcount
       passengers=[]
       for n in range(a):
           passengers.append({
            'name':row[n][8],
            'gender':row[n][9],
            'age':row[n][10],
            'seat_no':row[n][11],
            'no':n+1
           })
       data={
        'passengers':passengers,
        'date_of_booking':row[0][0],
        'no_of_passengers':row[0][1],
        'price_per_person':row[0][2],
        'total_price':row[0][2]*row[0][1],
        'company':row[0][3],
        'time_from':row[0][4].strftime("%H:%M"),
        'time_to':row[0][5].strftime("%H:%M"),
        'from_p':row[0][6],
        'to_p':row[0][7],
        'image':image,
        'firstname':firstname,
        'lastname':lastname,
        'wallet':wallet,
        'email':email,
        'userId':userId,
        'type':type_of_transport,
        'booking_id':bookingId,
        'status':row[0][12],
        'date_from':row[0][13],
        'date_to':row[0][14],
        'booking_Id':bookingId
        }
       context = data
       response = HttpResponse(content_type='application/pdf')
       response['Content-Disposition'] = 'inline; filename="booking_details.pdf"'
       template = get_template(template_path)
       html = template.render(context)
       pdf = pisa.CreatePDF(html,dest=response)
       print(type(pdf))
        
       if pdf.err:
          return HttpResponse('We had some errors <pre>' + html + '</pre>')
       return response
 elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
 else:
        return render(request,'authentication/error.html')
    

