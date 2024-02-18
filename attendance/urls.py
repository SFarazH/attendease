from django.urls import path
from . import views
from .views import index
from .views import loginDetails
from .views import error_page
from .views import displayAttendance

urlpatterns = [
    path("", index),
    path('sem/', loginDetails, name='loginDetails'),
    path('result/', displayAttendance, name='displayAttendance'),
    path('error/',error_page, name = 'error_page')
]