"""voyage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from authentication import views


urlpatterns = [
    # authentication urls
    path('admin/', admin.site.urls),
    path('',views.Home,name='home'),
    path('login/',views.Log_In,name='auth-login'),
    path('login/forgotpassword',views.Forgot_Password,name='forgot_password'),
    path('login/forgotpassword/<email>/resetpassword',views.Reset_Password,name='reset password'),
    path('signup/',views.Sign_Up,name='auth-signup'),
    path('login/<userId>/<email>/profile',views.Profile,name='profile'),
    path('login/<userId>/<email>',views.user,name='user'),
    path('login/admin/<userId>/<email>',views.admin,name='admin'),
    path('login/<userId>/<email>/changepassword',views.ChangePassword, name="changepassword"),
    path('login/admin/<userId>/<email>/changepassword',views.Admin_ChangePassword, name="admin-changepassword"),

    #flights views urls
    path('login/<userId>/<email>/flights',views.Flights,name='flights'),
    path('login/<userId>/<email>/flights/search/',views.Flights_Search,name='flights_search'),
    path('login/<userId>/<email>/flights/book/',views.Flights_Book,name='flights_book'),

  


    #buses views urls
    path('login/<userId>/<email>/buses',views.Buses,name='buses'),
    path('login/<userId>/<email>/buses/search/',views.Buses_Search,name='buses_search'),
    path('login/<userId>/<email>/buses/book/',views.Buses_Book,name='buses_book'),
 

    #bookings views urls
    path('login/<userId>/<email>/mybookings',views.My_Bookings,name='my_bookings'),
    path('login/<userId>/<email>/mybookings/<type_of_transport>/<bookingId>/details',views.Booking_Details,name="booking_details"),
    path('login/<userId>/<email>/mybookings/<type_of_transport>/<bookingId>/details/pdf',views.View_ticket_as_PDF,name="booking_details_as_PDF"),

    #admin views urls
    path('login/admin/<userId>/<email>/flights',views.Admin_Flights,name='admin-flights'),
    path('login/admin/<userId>/<email>/flights/list',views.Admin_Flights_List,name='admin-flights-list'),
    path('login/admin/<userId>/<email>/flights/details',views.Admin_Flights_Details,name='admin-flights-details'),
    path('login/admin/<userId>/<email>/flights/schedule',views.Admin_Flights_Schedule,name='admin-flights-schedule'),

    path('login/admin/<userId>/<email>/buses',views.Admin_Buses,name='admin-buses'),
    path('login/admin/<userId>/<email>/buses/list',views.Admin_Buses_List,name='admin-buses-list'),
    path('login/admin/<userId>/<email>/buses/details',views.Admin_Buses_Details,name='admin-buses-details'),
    path('login/admin/<userId>/<email>/buses/schedule',views.Admin_Buses_Schedule,name='admin-buses-schedule'),

    path('login/admin/<userId>/<email>/routes',views.Admin_Routes,name='admin-routes')





]
