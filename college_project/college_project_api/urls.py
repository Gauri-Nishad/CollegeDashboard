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
from college_project_api.views import *

urlpatterns = [
    
    
    # path('register', register, name='register'),
    path('login', login_view),
    path('logout', logout_view),
    #url for role
    path('add_role',add_role),
    path('update_role',update_role),
    path('get_role',get_role),
    path('get_role_list',get_role_list),
    path('delete_role',delete_role),
    #user api
    path('adduser',add_user),
    path('update_user',update_user),
    path('get_user',get_user),
    path('get_user_list',get_user_list),
    path('delete_user',delete_user),

    # subjects
    path('get_subjects_list',get_subjects_list),

    path('students',StudentList.as_view(),name='student-list-create'),
    path('studentdetail/<int:pk>',StudentDetail.as_view(),name='student-list-create'),
    # path('subjects',subjects,name='subjects')
   
]
