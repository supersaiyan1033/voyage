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


def Home(request):
    return render(request, 'authentication/home.html')


def Log_In(request):
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


def Profile(request, userId, email):
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


def ChangePassword(request, userId, email):
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


def Flights(request, userId, email):

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


def Flights_Search(request, userId, email):

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
        Indigo = request.POST.get('Indigo')
        AirAsia = request.POST.get('AirAsia')
        SpiceJet = request.POST.get('SpiceJet')
        TruJet = request.POST.get('TruJet')
        AirIndia = request.POST.get('AirIndia')
        total = ['AirAsia', 'Indigo', 'SpiceJet', 'TruJet', 'AirIndia']
        temp = [Indigo, AirAsia, SpiceJet, TruJet, AirIndia]
        unchecked = []
        print(temp)
        for company in temp:
            if company != None:
                companies.append(company)

        unchecked = [i for i in total +
                     companies if i not in total or i not in companies]
        companies = tuple(companies)
        print(companies)
        passengers = int(request.GET.get('travellers'))
        minm_price = int(request.POST.get("minm_price"))
        maxm_price = int(request.POST.get("maxm_price"))
        print(minm_price, type(minm_price), maxm_price, type(maxm_price))
        error_type_1 = None
        error_type_2 = None
        cursor = connection.cursor()
        if len(companies) != 0:
            cursor.execute("""select Date_Pk,Company,from_p,to_p,Time_From,Time_To,Price,no_of_seats_vacant
             FROM date_pk JOIN flight_specific ON date_pk.KID=flight_specific.KID JOIN route ON route.RID=flight_specific.RID JOIN flight ON flight.Flight_No=flight_specific.Flight_No
             WHERE date_from=%s AND from_p=%s AND to_p=%s AND Price BETWEEN %s AND %s  AND Company IN %s""", (date, from_p, to_p, minm_price, maxm_price, companies))
            error_type_1 = 1
        else:
            cursor.execute("""select Date_Pk,Company,from_p,to_p,Time_From,Time_To,Price,no_of_seats_vacant
             FROM date_pk JOIN flight_specific ON date_pk.KID=flight_specific.KID JOIN route ON route.RID=flight_specific.RID JOIN flight ON flight.Flight_No=flight_specific.Flight_No
             WHERE date_from=%s AND from_p=%s AND to_p=%s AND Price BETWEEN %s AND %s """, (date, from_p, to_p, minm_price, maxm_price))
            error_type_2 = 1
        a = cursor.rowcount
        companies = list(companies)
        row = cursor.fetchall()
        if cursor.rowcount != 0:
            flights = []
            for n in range(a):

                flights.append({
                    'date_pk': row[n][0],
                    'company': row[n][1],
                    'from_p': row[n][2],
                    'to_p': row[n][3],
                    'time_from': row[n][4],
                    'time_to': row[n][5],
                    'price': row[n][6],
                    'available': row[n][7]
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
                    'companies': companies,
                    'unchecked': unchecked,
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
                'companies': companies,
                'unchecked': unchecked,
                'error_type_1': error_type_1,
                'error_type_2': error_type_2

            }
            return render(request, 'authentication/flights_search.html', data)
    else:
        cursor = connection.cursor()
        cursor.execute("""select Date_Pk,Company,from_p,to_p,Time_From,Time_To,Price,no_of_seats_vacant
        FROM date_pk JOIN flight_specific ON date_pk.KID=flight_specific.KID JOIN route ON route.RID=flight_specific.RID JOIN flight ON flight.Flight_No=flight_specific.Flight_No
        WHERE date_from=%s AND from_p=%s AND to_p=%s""", (date, from_p, to_p))
        a = cursor.rowcount
        row = cursor.fetchall()
        if cursor.rowcount != 0:
            flights = []
            for n in range(a):
                flights.append({
                    'date_pk': row[n][0],
                    'company': row[n][1],
                    'from_p': row[n][2],
                    'to_p': row[n][3],
                    'time_from': row[n][4],
                    'time_to': row[n][5],
                    'price': row[n][6],
                    'available': row[n][7]
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


def Flights_Book(request, userId, email):   
   if request.method == "POST":
      date_pk=request.GET.get("c1")
      date_pk=int(date_pk)
      passengers=(request.GET.get("c2"))
      passengers=int(passengers)
      cursor = connection.cursor()
      cursor.execute("""SELECT wallet FROM users WHERE userID=%s""", [userId])
      row = cursor.fetchall()
      wallet = row[0][0]
      cursor = connection.cursor()
      cursor.execute("""SELECT Price,from_p,to_p,date_from FROM date_pk JOIN flight_specific ON date_pk.KID=flight_specific.KID JOIN route ON flight_specific.RID=route.RID WHERE Date_PK=%s""", [date_pk])
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
         cursor.execute("""INSERT INTO ticket(User_ID,Date_of_booking,Date_PK,No_of_passengers) VALUES(%s,%s,%s,%s)""",(userId,date_time,date_pk, passengers))
         cursor = connection.cursor()
         cursor.execute("""SELECT Booking_ID FROM ticket WHERE User_ID=%s and Date_of_booking=%s""", (userId,date_time))
         row = cursor.fetchall()
         booking_id = row[0][0]
         cursor = connection.cursor()
         cursor.execute("""INSERT INTO transaction(booking_ID) VALUES(%s)""",[booking_id])
         cursor = connection.cursor()
         cursor.execute("""SELECT no_of_seats_vacant,Total_seats FROM date_pk WHERE Date_PK=%s""", [date_pk])
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
         cursor.execute("""UPDATE date_pk SET no_of_seats_vacant=%s WHERE Date_PK=%s""",(no_of_seats_vacant,date_pk))
         messages.success(request,"Booking Successful!Check Your Ticket In My Bookings")
         return redirect("http://127.0.0.1:8000/login/{}/{}".format(userId,email))
      else:
          messages.success(request,"No Sufficient Money For Transaction In Wallet!")
          return redirect("http://127.0.0.1:8000/login/{}/{}/flights/search/?startfrom={}&destination={}&dateOfTravel={}&travellers={}".format(userId, email, from_p, to_p,date_from,passengers))         
   else:
      date_pk=request.GET.get("c1")
      date_pk=int(date_pk)
      passengers=(request.GET.get("c2"))
      passengers=int(passengers)
      cursor=connection.cursor()
      cursor.execute("""SELECT firstname,lastname,wallet FROM users WHERE userID=%s""", [userId])
      row=cursor.fetchall()
      firstname=row[0][0]
      lastname=row[0][1]
      wallet=row[0][2]
      cursor=connection.cursor()
      cursor.execute("""SELECT Company,from_p,to_p,Time_From,Time_To,Price,no_of_seats_vacant,date_from FROM date_pk JOIN flight_specific ON date_pk.KID=flight_specific.KID JOIN route ON route.RID=flight_specific.RID JOIN flight ON flight.Flight_No=flight_specific.Flight_No WHERE Date_Pk=%s""", [date_pk])
      row=cursor.fetchall()
      company=row[0][0]
      from_p=row[0][1]
      to_p=row[0][2]
      time_from=row[0][3]
      time_to=row[0][4]
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
            'date_pk':date_pk
        }        
      if passengers<=available:
         return render(request, 'authentication/flights_book.html', data)        
      else:
         messages.success(request, 'No.of passengers excede available no.of seats!')
         return redirect('http://127.0.0.1:8000/login/{}/{}/flights/search/?startfrom={}&destination={}&dateOfTravel={}&travellers={}'.format(userId, email, from_p, to_p, date_from, passengers))

# Create your views here.
