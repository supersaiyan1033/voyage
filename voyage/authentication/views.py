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
def myFunc(e):
  return e['date_of_booking']

# authentication views starts here

def Home(request):
    if request.session.get('email')!=None:
        email = request.session.get('email')
        userId = request.session.get('userId')
        url = "login/{}/{}".format(userId,email)
        return redirect(url)
    else:
      return render(request, 'authentication/home.html')


def Log_In(request):
    request.session.flush()
    request.session.clear_expired()
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE email= %s""", [email])
        row = cursor.fetchall()
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
        }

        if cursor.rowcount == 1:
            dbpassword = row[0][6]
            print(dbpassword)
            if bcrypt.checkpw(password.encode('utf8'), dbpassword.encode('utf8')):
                messages.success(request, 'Login successful!!')
                request.session['email'] = email
                request.session['userId'] = row[0][7]
                url = "{}/{}".format(data["userId"], data["email"])
                return redirect(url)
            else:
                messages.success(
                    request, 'incorrect password please try again!!')
                return render(request, 'authentication/login.html')
        else:
            messages.success(
                request, 'Account does not exist with the entered credentials!! signup to create an account')
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
        password = bcrypt.hashpw(password.encode(
            'utf8'), bcrypt.gensalt(rounds=12))

        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE email = %s""", [email])
        row = cursor.fetchall()
        if cursor.rowcount == 0:
            cursor.execute("""INSERT INTO users (firstname,lastname,gender,address,mobileno,email,password,DOB) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                           (firstname, lastname, gender, address, mobileno, email, password, DOB))
            messages.success(request, 'Sign Up successful!')
            return redirect('http://127.0.0.1:8000/login')
        else:
            messages.success(
                request, 'User with the entered email already exists!!!')
            return render(request, 'authentication/signup.html')
    else:
        return render(request, 'authentication/signup.html')


def user(request, userId, email):
 if request.session.get('email')!=None:
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
 else:
     return render(request,'authentication/error.html')


def Profile(request, userId, email):
 if request.session.get('email')!=None:
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
            return redirect('http://127.0.0.1:8000/login/{}/{}'.format(data["userId"], data["email"]))
        else:
            messages.success(request, 'incorrect password please try again!!')
            return render(request, 'authentication/profile.html', data)
    else:
        return render(request, "authentication/profile.html", data)
 else:
     return render(request,'authentication/error.html')


def ChangePassword(request, userId, email):
 if request.session.get('email')!=None:
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
                return redirect('http://127.0.0.1:8000/login/{}/{}'.format(userId, email))
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

# authentication views ends here flights part begins.

def Flights(request, userId, email):
 if request.session.get('email')!=None:
    if request.method == "POST":
        from_p = request.POST.get("startfrom")
        to_p = request.POST.get("destination")
        date = request.POST.get("dateOfTravel")
        passengers = request.POST.get("travellers")
        return redirect('http://127.0.0.1:8000/login/{}/{}/flights/search/?startfrom={}&destination={}&dateOfTravel={}&travellers={}'.format(userId, email, from_p, to_p, date, passengers))

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
        return render(request, 'authentication/flights.html', data)
 else:
     return render(request,'authentication/error.html')


def Flights_Search(request, userId, email):
 if request.session.get('email')!=None:
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
        temp = []
        companies = []
        from_p = request.GET.get('startfrom')
        to_p = request.GET.get('destination')
        date = request.GET.get('dateOfTravel')
        # Indigo = request.POST.get('Indigo')
        # AirAsia = request.POST.get('AirAsia')
        # SpiceJet = request.POST.get('SpiceJet')
        # TruJet = request.POST.get('TruJet')
        # AirIndia = request.POST.get('AirIndia')
        # total = ['AirAsia', 'Indigo', 'SpiceJet', 'TruJet', 'AirIndia']
        # temp = [Indigo, AirAsia, SpiceJet, TruJet, AirIndia]
        # unchecked = []
        # print(temp)
        # for company in temp:
        #     if company != None:
        #         companies.append(company)

        # unchecked = [i for i in total +
        #              companies if i not in total or i not in companies]
        # companies = tuple(companies)
        # print(companies)
        passengers = int(request.GET.get('travellers'))
        minm_price = int(request.POST.get("minm_price"))
        maxm_price = int(request.POST.get("maxm_price"))
        print(minm_price, type(minm_price), maxm_price, type(maxm_price))
        cursor = connection.cursor()
        # if len(companies) != 0:
        #     cursor.execute("""select FSID,Company,from_p,to_p,Time_From,Time_To,Price,no_of_seats_vacant
        #      FROM flight_schedule JOIN flight_specific ON flight_schedule.Flight_No=flight_specific.Flight_No JOIN route ON route.RID=flight_specific.RID JOIN flight ON flight.Flight_ID=flight_specific.Flight_ID
        #      WHERE date_from=%s AND from_p=%s AND to_p=%s AND Price BETWEEN %s AND %s  AND Company IN %s""", (date, from_p, to_p, minm_price, maxm_price, companies))
        # else:
        cursor.execute("""select FSID,Company,from_p,to_p,Time_From,Time_To,Price,no_of_seats_vacant
             FROM flight_schedule JOIN flight_specific ON flight_schedule.Flight_No=flight_specific.Flight_No JOIN route ON route.RID=flight_specific.RID JOIN flight ON flight.Flight_ID=flight_specific.Flight_ID
             WHERE date_from=%s AND from_p=%s AND to_p=%s AND Price BETWEEN %s AND %s """, (date, from_p, to_p, minm_price, maxm_price))
        a = cursor.rowcount
        # companies = list(companies)
        row = cursor.fetchall()
        if cursor.rowcount != 0:
            flights = []
            for n in range(a):

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
                    # 'companies': companies,
                    # 'unchecked': unchecked,
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
                # 'companies': companies,
                # 'unchecked': unchecked,

            }
            return render(request, 'authentication/flights_search.html', data)
    else:
        cursor = connection.cursor()
        cursor.execute("""select FSID,Company,from_p,to_p,Time_From,Time_To,Price,no_of_seats_vacant
        FROM flight_schedule JOIN flight_specific ON flight_schedule.Flight_No=flight_specific.Flight_No JOIN route ON route.RID=flight_specific.RID JOIN flight ON flight.Flight_ID=flight_specific.Flight_ID
        WHERE date_from=%s AND from_p=%s AND to_p=%s""", (date, from_p, to_p))
        a = cursor.rowcount
        row = cursor.fetchall()
        if cursor.rowcount != 0:
            flights = []
            for n in range(a):
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
 else:
     return render(request,'authentication/error.html')


def Flights_Book(request, userId, email):
 if request.session.get('email')!=None:
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
      cursor.execute("""SELECT Price,from_p,to_p,date_from FROM flight_schedule JOIN flight_specific ON flight_schedule.Flight_No=flight_specific.Flight_No JOIN route ON flight_specific.RID=route.RID WHERE FSID=%s""", [flight_schedule])
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
         cursor.execute("""INSERT INTO ticket(User_ID,Date_of_booking,FSID,No_of_passengers) VALUES(%s,%s,%s,%s)""",(userId,date_time,flight_schedule,passengers))
         cursor = connection.cursor()
         cursor.execute("""SELECT Booking_ID FROM ticket WHERE User_ID=%s and Date_of_booking=%s""", (userId,date_time))
         row = cursor.fetchall()
         booking_id = row[0][0]
         cursor = connection.cursor()
         cursor.execute("""INSERT INTO transaction(booking_ID) VALUES(%s)""",[booking_id])
         cursor = connection.cursor()
         cursor.execute("""SELECT no_of_seats_vacant,Total_seats FROM flight_schedule WHERE FSID=%s""", [flight_schedule])
         row = cursor.fetchall()
         vacant = row[0][0]
         total = row[0][1]
         for n in range(1,passengers+1):
            name = request.POST.get('name{}'.format(n))
            age = request.POST.get('age{}'.format(n))
            gender = request.POST.get('gender{}'.format(n))
            seat = total-vacant+n
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO passenger(Name,Gender,Age,Booking_ID,Seat_no) VALUES(%s,%s,%s,%s,%s)""",(name, gender, age, booking_id, seat))
         no_of_seats_vacant = vacant-passengers
         cursor = connection.cursor()
         cursor.execute("""UPDATE flight_schedule SET no_of_seats_vacant=%s WHERE FSID=%s""",(no_of_seats_vacant,flight_schedule))
         messages.success(request,"Booking Successful!Check Your Ticket In My Bookings")
         return redirect("http://127.0.0.1:8000/login/{}/{}".format(userId,email))
      else:
          messages.success(request,"No Sufficient Money For Transaction In Wallet!")
          return redirect("http://127.0.0.1:8000/login/{}/{}/flights/search/?startfrom={}&destination={}&dateOfTravel={}&travellers={}".format(userId, email, from_p, to_p,date_from,passengers))
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
      cursor.execute("""SELECT Company,from_p,to_p,Time_From,Time_To,Price,no_of_seats_vacant,date_from FROM flight_schedule JOIN flight_specific ON flight_schedule.Flight_No=flight_specific.Flight_No JOIN route ON route.RID=flight_specific.RID JOIN flight ON flight.Flight_ID=flight_specific.Flight_ID WHERE FSID=%s""", [flight_schedule])
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
              return redirect('http://127.0.0.1:8000/login/{}/{}/flights/search/?startfrom={}&destination={}&dateOfTravel={}&travellers={}'.format(userId, email, from_p, to_p, date_from, passengers))
      else:
          messages.success(request, 'please select valid number of passengers!')
          return redirect('http://127.0.0.1:8000/login/{}/{}/flights/search/?startfrom={}&destination={}&dateOfTravel={}&travellers={}'.format(userId, email, from_p, to_p, date_from, passengers))
 else:
     return render(request,'authentication/error.html')

#flights views ends here buses part starts here.

def Buses(request, userId, email):
 if request.session.get('email')!=None:
    if request.method == "POST":
        from_p = request.POST.get("startfrom")
        to_p = request.POST.get("destination")
        date = request.POST.get("dateOfTravel")
        passengers = request.POST.get("travellers")
        return redirect('http://127.0.0.1:8000/login/{}/{}/buses/search/?startfrom={}&destination={}&dateOfTravel={}&travellers={}'.format(userId, email, from_p, to_p, date, passengers))

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
 else:
     return render(request,'authentication/error.html')



def Buses_Search(request, userId, email):
 if request.session.get('email')!=None:
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
        temp = []
        companies = []
        from_p = request.GET.get('startfrom')
        to_p = request.GET.get('destination')
        date = request.GET.get('dateOfTravel')
        #bus companies 
        # Orange_Travels = request.POST.get('Orange Travels')
        # Amaravathi = request.POST.get('Amaravathi')
        # Deluxe = request.POST.get('Deluxe')
        # Chalo = request.POST.get('Chalo')
        # Aictsl = request.POST.get('AICTSL')
        # total = ['Orange Travels', 'Amaravathi', 'Deluxe', 'Chalo', 'AICTSL']
        # temp = [Orange_Travels, Amaravathi, Deluxe, Chalo, Aictsl]
        # unchecked = []
        # print(temp)
        # for company in temp:
        #     if company != None:
        #         companies.append(company)

        # unchecked = [i for i in total +
        #              companies if i not in total or i not in companies]
        # companies = tuple(companies)
        # print(companies)
        passengers = int(request.GET.get('travellers'))
        minm_price = int(request.POST.get("minm_price"))
        maxm_price = int(request.POST.get("maxm_price"))
        print(minm_price, type(minm_price), maxm_price, type(maxm_price))
        cursor = connection.cursor()
        # if len(companies) != 0:
        #     cursor.execute("""select BSID,Company,from_p,to_p,Time_From,Time_To,Price,no_of_seats_vacant
        #      FROM flight_schedule JOIN bus_specific ON bus_schedule.Bus_No=bus_specific.Bus_No JOIN route ON route.RID=bus_specific.RID JOIN bus ON bus.Bus_ID=bus_specific.Bus_ID
        #      WHERE date_from=%s AND from_p=%s AND to_p=%s AND Price BETWEEN %s AND %s  AND Company IN %s""", (date, from_p, to_p, minm_price, maxm_price, companies))
        # else:
        cursor.execute("""select BSID,Company,from_p,to_p,Time_From,Time_To,Price,no_of_seats_vacant
        FROM bus_schedule JOIN bus_specific ON bus_schedule.Bus_No=bus_specific.Bus_No JOIN route ON route.RID=bus_specific.RID JOIN bus ON bus.Bus_ID=bus_specific.Bus_ID
        WHERE date_from=%s AND from_p=%s AND to_p=%s AND Price BETWEEN %s AND %s """, (date, from_p, to_p, minm_price, maxm_price))
        a = cursor.rowcount
        # companies = list(companies)
        row = cursor.fetchall()
        if cursor.rowcount != 0:
            buses = []
            for n in range(a):

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
                    # 'companies': companies,
                    # 'unchecked': unchecked,
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
                # 'companies': companies,
                # 'unchecked': unchecked,

            }
            return render(request, 'authentication/buses_search.html', data)
    else:
        cursor = connection.cursor()
        cursor.execute("""select BSID,Company,from_p,to_p,Time_From,Time_To,Price,no_of_seats_vacant
        FROM bus_schedule JOIN bus_specific ON bus_schedule.Bus_No=bus_specific.Bus_No JOIN route ON route.RID=bus_specific.RID JOIN bus ON bus.Bus_ID=bus_specific.Bus_ID
        WHERE date_from=%s AND from_p=%s AND to_p=%s""", (date, from_p, to_p))
        a = cursor.rowcount
        row = cursor.fetchall()
        if cursor.rowcount != 0:
            buses = []
            for n in range(a):
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
 else:
     return render(request,'authentication/error.html')




def Buses_Book(request, userId, email):
 if request.session.get('email')!=None:
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
      cursor.execute("""SELECT Price,from_p,to_p,date_from FROM bus_schedule JOIN bus_specific ON bus_schedule.Bus_No=bus_specific.Bus_No JOIN route ON bus_specific.RID=route.RID WHERE BSID=%s""", [bus_schedule])
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
         cursor.execute("""INSERT INTO ticket_b(User_ID,Date_of_booking,BSID,No_of_passengers) VALUES(%s,%s,%s,%s)""",(userId,date_time,bus_schedule,passengers))
         cursor = connection.cursor()
         cursor.execute("""SELECT Booking_ID FROM ticket_b WHERE User_ID=%s and Date_of_booking=%s""", (userId,date_time))
         row = cursor.fetchall()
         
         booking_id = row[0][0]
         cursor = connection.cursor()
         cursor.execute("""INSERT INTO transaction_b(booking_ID) VALUES(%s)""",[booking_id])
         cursor = connection.cursor()
         cursor.execute("""SELECT no_of_seats_vacant,Total_seats FROM bus_schedule WHERE BSID=%s""", [bus_schedule])
         row = cursor.fetchall()
         vacant = row[0][0]
         total = row[0][1]
         for n in range(1,passengers+1):
            name = request.POST.get('name{}'.format(n))
            age = request.POST.get('age{}'.format(n))
            gender = request.POST.get('gender{}'.format(n))
            seat = total-vacant+n
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO passenger_b(Name,Gender,Age,Booking_ID,Seat_no) VALUES(%s,%s,%s,%s,%s)""",(name, gender, age, booking_id, seat))
         no_of_seats_vacant = vacant-passengers
         cursor = connection.cursor()
         cursor.execute("""UPDATE bus_schedule SET no_of_seats_vacant=%s WHERE BSID=%s""",(no_of_seats_vacant,bus_schedule))
         messages.success(request,"Booking Successful!Check Your Ticket In My Bookings")
         return redirect("http://127.0.0.1:8000/login/{}/{}".format(userId,email))
      else:
          messages.success(request,"No Sufficient Money For Transaction In Wallet!")
          return redirect("http://127.0.0.1:8000/login/{}/{}/buses/search/?startfrom={}&destination={}&dateOfTravel={}&travellers={}".format(userId, email, from_p, to_p,date_from,passengers))
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
      cursor.execute("""SELECT Company,from_p,to_p,Time_From,Time_To,Price,no_of_seats_vacant,date_from FROM bus_schedule JOIN bus_specific ON bus_schedule.Bus_No=bus_specific.Bus_No JOIN route ON route.RID=bus_specific.RID JOIN bus ON bus.Bus_ID=bus_specific.Bus_ID WHERE BSID=%s""", [bus_schedule])
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
              return redirect('http://127.0.0.1:8000/login/{}/{}/buses/search/?startfrom={}&destination={}&dateOfTravel={}&travellers={}'.format(userId, email, from_p, to_p, date_from, passengers))
      else:
          messages.success(request, 'please select valid number of passengers!')
          return redirect('http://127.0.0.1:8000/login/{}/{}/buses/search/?startfrom={}&destination={}&dateOfTravel={}&travellers={}'.format(userId, email, from_p, to_p, date_from, passengers))
 else:
     return render(request,'authentication/error.html')



#buses views ends here boking views starts here.

def My_Bookings(request,userId,email):
 if request.session.get('email')!=None:
    cursor = connection.cursor()
    cursor.execute("""SELECT firstname,lastname,wallet FROM users WHERE userID=%s""", [userId])
    user = cursor.fetchall()
    firstname = user[0][0]
    lastname = user[0][1]
    wallet = user[0][2]
    cursor.execute("""SELECT Booking_ID,Date_of_booking,No_of_passengers,Price,Company,Time_From,Time_To,from_p,to_p
    FROM ticket_b JOIN users ON ticket_b.User_ID=users.userID JOIN bus_schedule ON ticket_b.BSID=bus_schedule.BSID JOIN bus_specific ON bus_specific.Bus_No=bus_schedule.Bus_No JOIN bus ON bus_specific.Bus_ID=Bus.Bus_ID
    JOIN route ON route.RID=bus_specific.RID WHERE userID=%s ORDER BY Date_of_booking DESC""",[userId])
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
                'image':'fa fa-bus fa-3x',
                'type':'bus'
        })

    cursor.execute("""SELECT Booking_ID,Date_of_booking,No_of_passengers,Price,Company,Time_From,Time_To,from_p,to_p
    FROM ticket JOIN users ON ticket.User_ID=users.userID JOIN flight_schedule ON ticket.FSID=flight_schedule.FSID JOIN flight_specific ON flight_specific.Flight_No=flight_schedule.Flight_No JOIN flight ON flight_specific.Flight_ID=flight.Flight_ID
    JOIN route ON route.RID=flight_specific.RID WHERE userID=%s ORDER BY Date_of_booking DESC""",[userId])
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
                'image':'fa fa-plane fa-3x',
                'type':'flight'
            })
    bookings = []
    bookings = bus_bookings+flight_bookings
    
    if len(bookings)!=0:
        bookings.sort(reverse = True,key=myFunc)
        print(bookings)
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
 else:
     return render(request,'authentication/error.html')
# Create your views here.


def Booking_Details(request,userId,email,type_of_transport,bookingId):
 if request.session.get('email')!=None:
    cursor = connection.cursor()
    cursor.execute("""SELECT firstname,lastname,wallet FROM users WHERE userID=%s""", [userId])
    user = cursor.fetchall()
    firstname = user[0][0]
    lastname = user[0][1]
    wallet = user[0][2]
    if type_of_transport =='flight':
     cursor.execute("""SELECT Date_of_booking,No_of_passengers,Price,Company,Time_From,Time_To,from_p,to_p,Transaction_ID,Name,passenger.Gender,Age,Seat_no
     FROM ticket JOIN users ON ticket.User_ID=users.userID JOIN flight_schedule ON ticket.FSID=flight_schedule.FSID JOIN flight_specific ON flight_specific.Flight_No=flight_schedule.Flight_No JOIN flight ON flight_specific.Flight_ID=flight.Flight_ID
     JOIN route ON route.RID=flight_specific.RID JOIN passenger ON passenger.Booking_ID=ticket.Booking_ID JOIN transaction ON transaction.booking_ID = ticket.Booking_ID WHERE userID=%s AND ticket.Booking_ID=%s""",(int(userId),int(bookingId)) )
     row = cursor.fetchall()
     a = cursor.rowcount
     no_of_passengers = a
     passengers=[]
     for n in range(a):
        passengers.append({
            'name':row[n][9],
            'gender':row[n][10],
            'age':row[n][11],
            'seat_no':row[n][12],
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
        'transactionId':row[0][8],
        'image':'fa fa-plane fa-3x',
        'firstname':firstname,
        'lastname':lastname,
        'wallet':wallet,
        'email':email,
        'userId':userId
     }
     return render(request,'authentication/booking_details.html',data)
    elif type_of_transport =='bus':
     cursor.execute("""SELECT Date_of_booking,No_of_passengers,Price,Company,Time_From,Time_To,from_p,to_p,Transaction_ID,Name,passenger_b.Gender,Age,Seat_no
     FROM ticket_b JOIN users ON ticket_b.User_ID=users.userID JOIN bus_schedule ON ticket_b.BSID=bus_schedule.BSID JOIN bus_specific ON bus_specific.Bus_No=bus_schedule.Bus_No JOIN bus ON bus_specific.Bus_ID=bus.Bus_ID
     JOIN route ON route.RID=bus_specific.RID JOIN passenger_b ON passenger_b.Booking_ID=ticket_b.Booking_ID JOIN transaction_b ON transaction_b.booking_ID = ticket_b.Booking_ID WHERE userID=%s AND ticket_b.Booking_ID=%s""",(int(userId),int(bookingId)) )
     row = cursor.fetchall()
     a = cursor.rowcount
     no_of_passengers = a
     passengers=[]
     for n in range(a):
        passengers.append({
            'name':row[n][9],
            'gender':row[n][10],
            'age':row[n][11],
            'seat_no':row[n][12],
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
        'transactionId':row[0][8],
        'image':'fa fa-bus fa-3x',
        'firstname':firstname,
        'lastname':lastname,
        'wallet':wallet,
        'email':email,
        'userId':userId
     }
     return render(request,'authentication/booking_details.html',data)

 else:
     return render(request,'authentication/error.html')


