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
from authentication import views,admin_views ,auth_views


urlpatterns = [
    # authentication urls
    path('admin/', admin.site.urls),
    path('',auth_views.Home,name='home'),
    path('contactus',auth_views.Contact_us,name="Contact-us"),
    path('aboutus',auth_views.About_us,name="about-us"),
    path('login/',auth_views.Log_In,name='auth-login'),
    path('login/emailverification',auth_views.Verify_User_by_website,name='auth-verify'),
    path('login/forgotpassword',auth_views.Forgot_Password,name='forgot_password'),
    path('login/forgotpassword/<email>/resetpassword',auth_views.Reset_Password,name='reset password'),
    path('signup/',auth_views.Sign_Up,name='auth-signup'),
    path('profile',auth_views.Profile,name='profile'),
    path('home',auth_views.user,name='user'),
    path('admin/home',admin_views.admin,name='admin'),
    path('changepassword',auth_views.ChangePassword, name="changepassword"),
    path('admin/changepassword',auth_views.Admin_ChangePassword, name="admin-changepassword"),

    #flights views urls
    path('flights',views.Flights,name='flights'),
    path('flights/search/',views.Flights_Search,name='flights_search'),
    path('flights/book/',views.Flights_Book,name='flights_book'),

  


    #buses views urls
    path('buses',views.Buses,name='buses'),
    path('buses/search/',views.Buses_Search,name='buses_search'),
    path('buses/book/',views.Buses_Book,name='buses_book'),
 

    #bookings views urls
    path('mybookings',views.My_Bookings,name='my_bookings'),
    path('mybookings/<type_of_transport>/<bookingId>/details',views.Booking_Details,name="booking_details"),
    path('mybookings/<type_of_transport>/<bookingId>/details/pdf',views.View_ticket_as_PDF,name="booking_details_as_PDF"),

    #admin views urls
    path('admin/flights',admin_views.Admin_Flights,name='admin-flights'),
    path('admin/flights/list',admin_views.Admin_Flights_List,name='admin-flights-list'),
    path('admin/flights/details',admin_views.Admin_Flights_Details,name='admin-flights-details'),
    path('admin/flights/schedule',admin_views.Admin_Flights_Schedule,name='admin-flights-schedule'),

    path('admin/buses',admin_views.Admin_Buses,name='admin-buses'),
    path('admin/buses/list',admin_views.Admin_Buses_List,name='admin-buses-list'),
    path('admin/buses/details',admin_views.Admin_Buses_Details,name='admin-buses-details'),
    path('admin/buses/schedule',admin_views.Admin_Buses_Schedule,name='admin-buses-schedule'),

    path('admin/routes',admin_views.Admin_Routes,name='admin-routes'),

    path('admin/add',admin_views.View_Admin,name='admin-add')





]
