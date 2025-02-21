from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django.contrib.auth.models import User,Group
from rest_framework_simplejwt.tokens import RefreshToken
import re
from django.contrib.auth.hashers import make_password,check_password
from college_project_api.serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .models import User
# Create your views here.





@api_view(['POST'])
def login_view(request):
    data=request.data.copy()
    username = request.data.get('username')
    print("username;;;;", username )
    
    password=request.data.get('password')
    print("password;;;;",password)
    if not username:
        return Response({ 'msg': 'enter username'})
    if not password:
        return Response({ 'msg': 'enter password'})
    # if user.groups.filter(name =' Faculty').exists():
    # user = authenticate(username=username, password=password)
    user=User.objects.filter(username=username, is_active=True).first()
   
    print("user",user)
    # user
    if user :
    
        serializer = UserSerializer(user)
        print("dnknfnm",serializer.data)
        refresh_token=RefreshToken.for_user(user)
        access_token=refresh_token.access_token
        user_token=UserToken(user=user,access_token=access_token)
        user_token.save()
        if not check_password(password, user.password):
            return Response({'msg': 'Invalid username or password'})

    
        return Response({'msg': 'You have logged in successfully','accesstoken':str(access_token),'data': serializer.data,'n': 1})
    else:
        return Response({'msg': 'user not found','n': 0,})




# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
@api_view(['POST'])
def logout_view(request):
   
    token = request.data.get('access_token')
    print("Received token:", token)
    
    # Fetch the token from the database
    user_token = UserToken.objects.filter(access_token=token, is_active=True).first()
    print("User token:", user_token)
    
    if user_token:
        user_token.is_active = False
        user_token.save()
        return Response({"msg": "You have been successfully logged out.", "n": 1})
    else:
        return Response({"msg": "Token not found or already inactive.", "n": 0})





# Role views
 
@api_view(['POST'])
def add_role(request):
    data=request.data
    role_name=request.data.get('name')
    obj=Role.objects.filter()
    role_serializer=RoleSerializer(obj,many=True)
    for s in role_serializer.data:
        if s['name'].lower()==role_name.lower():
            return  Response({'msg':'role is already exist','n':0})
    serializer=RoleSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'data':serializer.data,'msg':'form submitted','n':1})
    else:
        return Response({'data':serializer.errors,'msg':'form not submitted','n':0})

@api_view(['POST'])
def update_role(request):
    data=request.data
    role_id=request.data.get('id')
    role_name=request.data.get('name')
    roleobj=Role.objects.get(id=role_id)    
    serializer=RoleSerializer(roleobj,data=data)
      

    obj=Role.objects.filter().exclude(id=role_id)
    role_serializer=RoleSerializer(obj,many=True)
    for c in role_serializer.data:
        if c['name'].lower()==role_name.lower():
            return  Response({'msg':'role is already exist','n':0})
    if serializer.is_valid():
        serializer.save()
        return Response({'data':serializer.data,'msg':'form updated','n':1})
    else:
        return Response({'data':serializer.errors,'msg':'form not updated','n':0})
    
@api_view(['POST'])
def get_role(request):
    role_id=request.data.get('id')
    roleobj=Role.objects.filter(id=role_id).first()
    serializer=RoleSerializer(roleobj)
    return Response(serializer.data)


@api_view(['POST'])
def get_role_list(request):
    roleobj=Role.objects.filter(is_active=True).all()
    serializer=RoleSerializer(roleobj,many=True)
    return Response(serializer.data)


@api_view(['POST'])
def delete_role(request):
    role_id=request.data.get('id')
    roleobj=Role.objects.filter(id=role_id,is_active=True).first()
    roleobj.is_active=False
    roleobj.save()
    return Response({'msg':'role deleted','n':1})


@api_view(['GET'])
def get_subjects_list(request):
    subjobj=Subjects.objects.all()
    serializer=SubjectsSerializer(subjobj,many=True)
    return Response(serializer.data)
      

@api_view(['POST'])
def add_user(request):
    # requestdata=request.data.copy()
    data=request.data.copy()
    gender=data.get('gender')
    data['password']=make_password(data['password'])
    data['is_active']=True
    valid_genders = ['male', 'female','Female','Male']
    dob=data.get('dob')
    email=data.get('email')
    contact_number=data.get('contact_number')
    username=data.get('username')
   
    if gender not in valid_genders:
        return Response({'msg': 'Please select gender','n':0})
    
    if not dob:
        return Response({'msg': 'Date of birth is required.','n':0})
    
    # print("ppp",contact_number,len(str(contact_number)))
    if len(str(contact_number)) != 10:
        return Response({'msg':'mobile number must be 10 digit','n':0})
    
    existing_number = User.objects.filter(contact_number=contact_number).first()
    if existing_number !=None:
        return Response({'msg': 'mobile number already exists','n':0})
    username = User.objects.filter(username=username).first()
    if username !=None:
        return Response({'msg': 'username is already exists','n':0})

    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, email) :
        return Response({'msg': 'Incorrect email id','n':0})
    
    
    existing_email=User.objects.filter(email=email).first()
    if existing_email !=None:
        return Response({'msg':'email already exists','n':0})

    serializer=UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()   
        return Response({'data':serializer.data,'n':1,'msg':'user added'})
    else:
        print("usererroo",serializer.errors)
        return Response({'data':serializer.errors,'n':0,'msg':'form not submitted'})
    
 
@api_view(['POST'])
def get_user(request):
     
    # datalist=[]
    id =request.data.get('id')
    obj=User.objects.filter(id=id).first()
    serializer=UserSerializer(obj)
    # for s in [serializer.data]:
    #     s['country'] = int(s['country'])
    #     datalist.append(s)
    return Response(serializer.data)
  

@api_view(['GET'])
def get_user_list(request):
    obj=User.objects.filter(is_active=True).all()
    serializer=UserSerializer(obj,many=True )
    # for s in serializer.data:
    #     obj=Subjects.objects.filter(id=s['subjects']).first()
        
    #     s['subjects']=obj.name
       

     
    return Response(serializer.data)

@api_view(['POST'])
def update_user(request):
    data=request.data.copy()
    print("daata",data)
    user_id =request.data.get('id')
    obj=User.objects.get(id=user_id) 
    data['password']=make_password(data['password'])
    gender=request.data.get('gender')
    email=request.data.get('email')
    contact_number=request.data.get('contact_number')
    dob=request.data.get('dob')
    pic=request.data.get('profile_pic')
    print("pppppiiiiiccccc",pic)
    valid_genders = ['male', 'female','Female','Male']
    
   
    if gender not in valid_genders:
        return Response({'msg': 'Please select gender','n':0})
    
    if not dob:
        return Response({'msg': 'Date of birth is required.','n':0})
    
    if len(str(contact_number)) != 10:
        return Response({'msg':'mobile number must be 10 digit','n':0})
    
    existing_number = User.objects.filter(contact_number=contact_number).exclude(id=request.data.get('id')).first()
    if existing_number !=None:
         return Response({'msg': 'mobile number already exists','n':0})
    
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, email) :
        return Response({'msg': 'Incorrect email id','n':0})
    
    existing_email=User.objects.filter(email=email).exclude(id=request.data.get('id')).first()
    if existing_email !=None:
        return Response({'msg':'email already exists','n':0})

    serializer=UserSerializer(obj,data=data,partial=True)
    if serializer.is_valid():
       
       serializer.save()
       return Response({'data':'serializer.data','n':1,'msg':'form updated'})
    else:
       return Response({'data':'serializer.errors','n':0,'msg':'form not updated'})


@api_view(['POST'])
def delete_user(request):
    
    id =request.data.get('id')
    obj=User.objects.filter(id=id,is_active = True).first()
    
    obj.is_active == False
    obj.save()
    return Response({'msg':'user deleted','n':1})
    











class StudentList(APIView): 
    """ 
    List all students, or create a new student 
    """
  
    def get(self, request): 
        students = Students.objects.all() 
        serializer = StudentSerializer(students, many=True) 
        return Response(serializer.data) 
  
    def post(self, request): 
        serializer = StudentSerializer(data=request.data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response({"data":serializer.data,"msg":"student created succesfully!","n":1}) 
        return Response({"error":serializer.errors,"msg":"something went wrong!!","n":0}) 
  
class StudentDetail(APIView): 
    """ 
    Retrieve, update or delete a student instance 
    """

    def get(self, request, pk): 
        student = Students.objects.filter(pk=pk).first() 
        serializer = StudentSerializer(student) 
        return Response(serializer.data) 
  
    def put(self, request, pk, format=None):
        profile_pic=request.data.get('profile_pic')
        first_name=request.data.get('first_name')  
        last_name=request.data.get('last_name')  
        dob=request.data.get('dob')  
        gender=request.data.get('gender')  
        blood_group=request.data.get('blood_group')  
        contact_number=request.data.get('contact_number')
        address=request.data.get('address')    
        student = Students.objects.filter(pk=pk).first() 
        serializer = StudentSerializer(student, data=request.data) 
        if not profile_pic:
            return Response({'msg':"profile picture is required","n":0})
        if not first_name:
            return Response({'msg':"first name is required","n":0})
        if not last_name:
            return Response({'msg':"last name is required","n":0})
        if not dob:
            return Response({'msg':"dob is required","n":0})
        if not gender:
            return Response({'msg':"gender is required","n":0})
    
        if not blood_group:
            return Response({'msg':"blood group is required","n":0})
        if not contact_number:
            return Response({'msg':"contact number is required","n":0})
        if not address:
            return Response({'msg':"address is required","n":0})
        if serializer.is_valid(): 
            serializer.save() 
        if serializer.is_valid():
            serializer.save()
            return Response( {"msg":"post updated","data":serializer.data,"n":1})
        return Response({"msg":"something went wrong!!","error":serializer.errors,"n":0})



# @api_view(['POST'])
# def subjects(request):
#     subjects = Subjects.objects.all() 
#     serializer = SubjectsSerializer(subjects, many=True) 
#     return Response(serializer.data) 
