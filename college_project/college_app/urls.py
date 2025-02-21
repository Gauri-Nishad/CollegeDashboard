"""
URL configuration for college_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from college_app.views import *
urlpatterns = [
    # path('',login,name="login"),
    path('', login_view, name='login'),
    path('logout_front',logout_method, name='logout'),
    path('dashboard',dashboard, name='dashboard'),
    path('base',base,name="base"),
    path("updateuser/<int:id>",updateuser,name="updateuser"),
    path("deleteuser/<int:id>",deleteuser,name="deleteuser"),
    path("add_user",add_user,name="add_user"),
    path("getuser/<int:id>",getuser,name="getuser")
    # path('teacher_dashboard',teacher_dashboard,name='teacher_dashboard'),
    # path('student_dashboard',student_dashboard,name='student_dashboard'),
    # path('add_student_page',add_student,name='add_student')

   
]
