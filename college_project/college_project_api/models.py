from django.db import models
from django.utils.timezone import now
# from django.contrib.auth.models import User
import datetime
# Create your models here.

class Subjects(models.Model):
    name=models.CharField(max_length=100,unique=True)
    # created_on=models.DateField(blank=True)
    # created_by=models.IntegerField()
    # deleted_on=models.DateField(blank=True)
    # deleted_by=models.IntegerField()
    # modified_on=models.DateField(blank=True)
    # modified_by=models.IntegerField()

class Role(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)

class User(models.Model):
    profile_pic=models.ImageField(upload_to='images/',null=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    dob=models.DateField(null=True,blank=True)
    gender=models.CharField(max_length=100)
    blood_group=models.CharField(max_length=100)
    contact_number=models.BigIntegerField(default=None)
    email=models.EmailField(max_length=254)
    address=models.CharField(max_length=100,default=None)
    role=models.ForeignKey(Role,on_delete=models.CASCADE)
    subjects=models.ManyToManyField(Subjects,related_name="subjects",default=list,blank=True)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100,blank=True)
    is_active = models.BooleanField(default=True)

class UserToken(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=500, unique=True)
    is_active = models.BooleanField(default=True)

class Students(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE,default=1)
    profile_pic=models.ImageField(upload_to='static/img', height_field=None, width_field=None, max_length=None)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    dob=models.DateField(auto_now=False, auto_now_add=False)
    gender=models.CharField(max_length=100, choices=[('Male', 'Male'), ('Female', 'Female')])
    blood_group=models.CharField(max_length=100)
    contact_number=models.BigIntegerField(default=None)
    address=models.CharField(max_length=100,default=None)
    subjects=models.ManyToManyField(Subjects,related_name="students",null=True)
    # created_on=models.DateField(default=datetime.date.today)
    # created_by=models.IntegerField()
    # deleted_on=models.DateField(default=datetime.date.today)
    # deleted_by=models.IntegerField()
    # modified_on=models.DateField(default=datetime.date.today)
    # modified_by=models.IntegerField()

class Faculties(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE,default=1)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone_number=models.BigIntegerField()
    subjects = models.OneToOneField(Subjects, on_delete=models.CASCADE, related_name="faculty")
    student=models.ManyToManyField(Students,related_name="students")
    # created_on=models.DateField(default=now)
    # created_by=models.IntegerField()
    # deleted_on=models.DateField(default=now)
    # deleted_by=models.IntegerField()
    # modified_on=models.DateField(default=now)
    # modified_by=models.IntegerField()


# class Role(models.Model):
#     name=models.CharField(max_length=100)
#     description=models.CharField(max_length=100, null=True)
#     is_active = models.BooleanField(default=True)




