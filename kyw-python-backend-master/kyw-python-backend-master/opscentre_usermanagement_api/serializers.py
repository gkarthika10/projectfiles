from rest_framework import serializers

from auction_api.serializers import AuctionViewSerializer
from .models import *
from django.contrib.auth.hashers import check_password,make_password



class OpsTeamRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = OpsTeamRole
        fields = ['role_id','record_id','name']


class OpsTeamSerializer(serializers.ModelSerializer):

    def validate_password(self,password: str) -> str:
                return make_password(password)
    OpsRole = OpsTeamRoleSerializer(many=False)
    
    class Meta:
        model = OpsTeam
        fields = ['record_id','ops_id','first_name','last_name','email','roleName','active','approved','OpsRole']

    extra_kwargs = {
            'password':{'write_only': True}
        }
    

class OpsTeamCreateSerializer(serializers.ModelSerializer):

    def validate_password(self,password: str) -> str:
                return make_password(password)
    #OpsRole = OpsTeamRoleSerializer(many=False)
    class Meta:
        model = OpsTeam
        fields = ['first_name','last_name','record_id','OpsRole','email','password']

    extra_kwargs = {
            'password':{'write_only': True}
        }



class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["name", "website", "employer_details_id", "employer_team_count", "bgv_completed", "type"]

class RecruiterSerializer(serializers.ModelSerializer):
    account = AccountsSerializer(many=False)
    class Meta:
        model = Contact

#        fields = [
#            "member_id","account","first_name","last_name","email","mobile_phone","email_verified","role","status"
#        ]

        fields = [
            "member_id","account","first_name","last_name","email","mobile_phone","email_verified","role","status"
        ]
        extra_kwargs  ={
           "member_id":{'read_only': True},
           "password":{'write_only': True},
        } 



class EmpListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = [
            "member_id","first_name","last_name","email","mobile_phone","email_verified","role","status"
        ]
        extra_kwargs  ={
           "member_id":{'read_only': True},
           "password":{'write_only': True},
        } 

class CandidatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = [
            "record_id","first_name","last_name","email","phone","email_verification","screening_stages","created_date"
        ]


class CandProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateProfile
        #exclude = ["cand_id"]
        fields = [
            "record_id","current_employer","first_name","last_name","candidate_email","candidate_phone","auction_availability","background_verification","dob"
        ]
        extra_kwargs  ={
           "member_id":{'read_only': True},
           "password":{'write_only': True},
           "cand_id":{'read_only': True} 
        } 


class SRSerializer(serializers.ModelSerializer):
    opsteam = OpsTeamSerializer(many = False)
    auction = AuctionViewSerializer (many = False)
    candidate = CandidatesSerializer(many = False)
    recruiter = RecruiterSerializer(many = False)

    class Meta:
        model = ServiceRq
        fields = [
            "record_id","rq_id","status","create_dtime","create_time_stamp","detailed_notes","priority","short_desc","opsteam","auction","candidate","recruiter"
        ]

class SRCreateSerializer(serializers.ModelSerializer):
    #opsteam = OpsTeamSerializer(many = False)
    #auction = AuctionViewSerializer (many = False)
    #candidate = CandidatesSerializer(many = False)
    #recruiter = RecruiterSerializer(many = False)

    class Meta:
        model = ServiceRq
        fields = [
            "status","detailed_notes","priority","short_desc","opsteam","auction","candidate","recruiter"
        ]


class SRCommentSerializer(serializers.ModelSerializer):

    candidate = CandidatesSerializer(many = False)
    recruiter = RecruiterSerializer(many = False)
    ops_user = OpsTeamSerializer(many = False)

    class Meta:
        model = SR_comments
        fields = [
            "record_id","comment","create_dtime","candidate","recruiter","ops_user"
        ]

class SRCommentCreateSerializer(serializers.ModelSerializer):

    #candidate = CandidatesSerializer(many = False)
    #recruiter = RecruiterSerializer(many = False)
    #ops_user = OpsTeamSerializer(many = False)

    class Meta:
        model = SR_comments
        fields = [
            "comment","dtime","service_rq","candidate","recruiter","ops_user"
        ]
