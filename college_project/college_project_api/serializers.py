from rest_framework import serializers
from .models import *
# from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Role
        fields='__all__'

class FacultySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Faculties
        fields ='__all__'
    

class StudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Students
        fields ='__all__'
    
class SubjectsSerializer(serializers.ModelSerializer):
     class Meta:
        model = Subjects
        fields ='__all__'



