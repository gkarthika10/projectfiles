
from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import check_password,make_password
class CandidateSerializer(serializers.ModelSerializer):

    def validate_password(self,password: str) -> str:
                return make_password(password)

    class Meta:
        model = Candidate
        fields = ['record_id','first_name','last_name','phone','password','email','screening_stages']
        extra_kwargs = {
            'password':{'write_only': True},
            'screening_stages':{'read_only':True},
            'record_id': {'read_only': True}
        }

class EmployerSerializer(serializers.ModelSerializer):

    def validate_password(self,password: str) -> str:
                return make_password(password)

    class Meta:
        model = Employer
        fields = ['name','email','phone','website','password','screening_stage']
        extra_kwargs = {
            'password':{'write_only': True},
            'screening_stage':{'read_only':True}
        }



class EmployerProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =   Account

        fields = [
            "employer_details_id","name","type","billing_address","website","number_of_employees"
        ]
        extra_kwargs  ={
           "employer_details_id":{'read_only': True}
        } 

# class EmployerAccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = ["name"] 

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ["id"]

class EmployerAdminSerializer(serializers.ModelSerializer):

    def validate_password(self,password: str) -> str:
                return make_password(password)

    account = AccountSerializer(many=False)

    class Meta:
        model = Contact

        fields = [
            "member_id","account","first_name","last_name","email","mobile_phone","password","email_verified","role","status"
        ]
        extra_kwargs  ={
           "member_id":{'read_only': True},
           "password":{'write_only': True},
        } 


class EmployerAdminPostSerializer(serializers.ModelSerializer):

    def validate_password(self,password: str) -> str:
                return make_password(password)

    class Meta:
        model = Contact

        fields = [
            "member_id","account","first_name","last_name","email","mobile_phone","password","email_verified","role","status"
        ]
        extra_kwargs  ={
           "member_id":{'read_only': True},
           "password":{'write_only': True},
        }

class NotificationGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = [
            "message", "created_date"
        ]