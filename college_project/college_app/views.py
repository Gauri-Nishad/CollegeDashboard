from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
# from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from college_project_api.models import *
# # Create your views here.
login_url="http://127.0.0.1:8000/login"
register_url="http://127.0.0.1:8000/register"
logout_url="http://127.0.0.1:8000/logout"
students_url="http://127.0.0.1:8000/students"
# subject_list_url="http://127.0.0.1:8000/subjects"
log_out_url="http://127.0.0.1:8000/logout"

user_list_url="http://127.0.0.1:8000/get_user_list"
subjects_list_url="http://127.0.0.1:8000/get_subjects_list"

update_user_url="http://127.0.0.1:8000/update_user"
delete_user_url="http://127.0.0.1:8000/delete_user"

add_user_url="http://127.0.0.1:8000/adduser"
get_user_url="http://127.0.0.1:8000/get_user"
role_list_url="http://127.0.0.1:8000/get_role_list"
def login_view(request):
    data=request.POST.copy()
    if request.method == 'POST':
    
        login_request= requests.post(login_url,data=data)
        login_response=login_request.json()
      
        if login_response['n'] == 1:
            request.session['role']= login_response['data']['role']
            request.session['userid']= login_response['data']['id']
            request.session['access_token']= login_response['accesstoken']
            print(";;;;;;;;;",login_response['data']['role'])
            messages.success(request,login_response['msg'])
            return redirect("college_app:dashboard")  
        
        else:
            messages.error(request,login_response['msg'])
            return redirect("college_app:login")

    return render(request, 'login.html')


def logout_method(request):
    data={}
    data['access_token'] = request.session.get('access_token')
    access_token = request.session.get('access_token')
    print("aaaaaaaaaaa",access_token)
    if not access_token:
        messages.error(request, "No active session found.")
        return redirect('college_app:login')

    data = {'access_token': access_token}
    
    log_out_request=requests.post(log_out_url,data=data)
    print('log_out_request',log_out_request)
    log_out_response=log_out_request.json()   
    print('rspons...',log_out_response)
    if log_out_response['n']==1:
        messages.success(request,log_out_response['msg'])
        request.session.flush()
        return redirect('college_app:login')
    return redirect('college_app:login')

def dashboard(request):
    session_data = request.session.items()
    print("llllll",session_data)
    role_id = request.session.get('role')
    userid=request.session.get('userid')
    print("useridddd",userid)
    if not role_id:
        messages.error(request, "Please login again!")
        return redirect('college_app:login')
    user = User.objects.select_related('role').filter(role_id=role_id).first()
    print("////",user)
    if not user:
        messages.error(request, "User not found.")
        return redirect('college_app:login')
    role_name = user.role.name
    role_id=user.role.id
    
   
    print("rrrr",role_name)
    if role_name=="Admin":
        user_list_rquest=requests.get(user_list_url)
        print(" user_list_rquest", user_list_rquest)
        user_list_response=user_list_rquest.json()
        print("user_list_response",user_list_response)

        subjects_list_rquest=requests.get(subjects_list_url)
        print(" subjects_list_rquest", subjects_list_rquest)
        subjects_list_response=subjects_list_rquest.json()
        print("subjects_list_response",subjects_list_response)
    
    if  role_name=="Student":
        user_list_response=[]
       
        user_list_rquest=requests.get(user_list_url)
        print(" user_list_rquest", user_list_rquest)
        all_user=user_list_rquest.json()
        print("user_list_response",user_list_response)

        role_list_rquest=requests.post(role_list_url)
        print(" role_list_rquest", role_list_rquest)
        role_list_response=role_list_rquest.json()
        role=[role for role in role_list_response]
        subjects_list_rquest=requests.get(subjects_list_url)
        print(" subjects_list_rquest", subjects_list_rquest)
        subjects_list_response=subjects_list_rquest.json()
        print("subjects_list_response",subjects_list_response)
        user_list_response=[student for student in all_user if student['id'] == userid]


    if  role_name=="Teacher":
        user_list_response=[]
        user_list_rquest=requests.get(user_list_url)
        print(" user_list_rquest", user_list_rquest)
        all_user=user_list_rquest.json()
        print("all_user",user_list_response)

        subjects_list_rquest=requests.get(subjects_list_url)
        print(" subjects_list_rquest", subjects_list_rquest)
        subjects_list_response=subjects_list_rquest.json()
        print("subjects_list_response",subjects_list_response)
        user_list_response=[student for student in all_user if student['role']==3]

    return render(request,"dashboard.html",{"users":user_list_response,"subjects":subjects_list_response,"role_id":role_id,"role":role_name})


def add_user(request):
    # data=request.data.copy()
    subjects_list_rquest=requests.get(subjects_list_url)
    print(" subjects_list_rquest", subjects_list_rquest)
    subjects_list_response=subjects_list_rquest.json()
    print("subjects_list_response",subjects_list_response)

    role_list_rquest=requests.post(role_list_url)
    print(" role_list_rquest", role_list_rquest)
    role_list_response=role_list_rquest.json()
    print("role_list_response",role_list_response)
    if request.method=="POST":
        selected_subject_ids = request.POST.getlist('subjects')
        print('selected_subject_ids/......',selected_subject_ids)
        if selected_subject_ids:
            request_data = request.POST.copy() 
            request_data['subjects'] = selected_subject_ids
           

            add_user_request=requests.post(add_user_url,data=request_data,files=request.FILES)
            print("add_user_request",add_user_request)
            add_user_response=add_user_request.json()
            print("add_user_response",add_user_response)
            
            if add_user_response['n']==1:
                messages.success(request,add_user_response['msg'])
                return redirect("college_app:dashboard")
            else:
                messages.error(request,add_user_response['msg'])
                return redirect("college_app:dashboard")
      
        
    return render(request,'add_user.html',{"subjects":subjects_list_response,"roles":role_list_response})







def updateuser(request,id):
    data=request.POST.copy()
    data['id']=id
    if request.method=="POST":
        update_user_request=requests.post(update_user_url,data=data,files=request.FILES)
        print("update_user_request",update_user_request)
        update_user_response=update_user_request.json()
        print("update_user_response",update_user_response)
        if update_user_response['n']==1:
            messages.success(request,update_user_response['msg'])
            return redirect("college_app:dashboard")
        else:
            messages.error(request,update_user_response['msg'])
            return redirect("college_app:dashboard")
    

    else:
        get_user_request=requests.post(get_user_url,data=data)
        get_user_response=get_user_request.json()
        role_list_rquest=requests.post(role_list_url)
        print(" role_list_rquest", role_list_rquest)
        role_list_response=role_list_rquest.json()
        print("role_list_response",role_list_response)
        subjects_list_rquest=requests.get(subjects_list_url)
        print(" subjects_list_rquest", subjects_list_rquest)
        subjects_list_response=subjects_list_rquest.json()
        print("subjects_list_response",subjects_list_response)
        return render(request,'update_user.html',{"user":get_user_response,"roles":role_list_response,"subjects":subjects_list_response})



def deleteuser(request,id):
    data={}
    data['id']=id
    delete_user_request=requests.post(delete_user_url,data=data)
    delete_user_response=delete_user_request.json()
    if delete_user_response['msg']==1:
        messages.success(request,delete_user_response['msg'])
        return redirect("college_app:dashboard")
    else:
        messages.error(request,delete_user_response['msg'])
        return redirect("college_app:dashboard")

# def teacher_dashboard(request):
      
#     return render(request,"teacher_dashboard.html")

# def add_student(request):
#     if not request.user.groups.filter(name='Faculty').exists():
#         messages.error(request, 'You are not authorized to access this page.')
#         return redirect('app:login')
#     subject_list=requests.post(subject_list_url)
#     subject_list_response=subject_list.json()
  
#     if request.method == 'POST':
#         # profile_pic = request.POST.get('title')
#         # first_name = request.POST.get('content')
#         # last_name = request.POST.get('last_name')
#         # dob = request.POST.get('dob')
#         # gender = request.POST.get('gender')
#         # blood_group = request.POST.get('blood_group')
#         # contact_number = request.POST.get('contact_number')
#         # address= request.POST.get('address')
#         selected_subject_ids = request.POST.getlist('subjects')
#         print('selected_subject_ids/......',selected_subject_ids)
#         if selected_subject_ids:
#             request_data = request.POST.copy()  # Make a copy of the POST data
#             request_data['subjects'] = selected_subject_ids
#             add_student_request=requests.post(students_url,data=request_data,files=request.FILES)
#             print('add_student_request///',add_student_request)
#             add_student_response=add_student_request.json()
            
#             print('add_student_response//', add_student_response)
#             if add_student_response['n']==1:
#                 messages.success(request,add_student_response['msg'])
#                 return redirect('college_app:add_student')
#             else:
#                 messages.error(request, add_student_response['msg'])
#                 return redirect('college_app:add_student') 
#         else:
#             messages.error(request, 'Please select at least one subject.')
#             return redirect('college_app:add_student')
#     return render(request,'add_student.html',{'subjects':subject_list_response})    

# def student_dashboard(request):
#     return render(request,"student_dashboard.html")




def getuser(request,id):
    data=request.POST.copy()
    data['id']=id
    get_user_request=requests.post(get_user_url,data=data)
    print("get_user_request",get_user_request)
    get_user_response=get_user_request.json()
    print("get_user_response",get_user_response)
    subjects_list_rquest=requests.get(subjects_list_url)
    print(" subjects_list_rquest", subjects_list_rquest)
    subjects_list_response=subjects_list_rquest.json()
    print("subjects_list_response",subjects_list_response)
    role_list_rquest=requests.post(role_list_url)
    print(" role_list_rquest", role_list_rquest)
    role_list_response=role_list_rquest.json()
    print("role_list_response",role_list_response)
    return render(request, 'viewuser.html',{"subjects":subjects_list_response,"user":get_user_response,"roles":role_list_response})







def base(request):
    session_data = request.session.items()
    print("llllll",session_data)

    role_id = request.session.get('role')
   
    user = User.objects.select_related('role').get(id=role_id)
   
    role_name = user.role.name
    role_id=user.role.id
    print("rrrr",role_name)
    return render(request,'base.html',{"role_name":role_name})