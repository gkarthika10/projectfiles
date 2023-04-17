
from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import check_password,make_password


class CandidateProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =   CandidateProfile

        fields = ['education','current_employer','current_ctc','candidate','first_name','last_name','resume_url','about','skills','experience',
        'projects','certifications','accomplishments','links','preferred_work_location','dob',
        'current_role','expected_role','current_address','permanent_address','relevant_experience','total_experience','notice_period','screening_stages'
        ]
        extra_kwargs  ={
           'record_id':{'read_only': True},
           'screening_stages':{'read_only': True}
          
        } 


class CandidateSerializer(serializers.ModelSerializer):

    profile = CandidateProfileSerializer(many=False)

    
    class Meta:
        model = Candidate
        fields = ['first_name','last_name','contact_no','email','screening_stages',]
        extra_kwargs = {
            'password':{'write_only': True},
            'screening_stages':{'read_only':True}
        }


class BidDetailSerializer(serializers.ModelSerializer):
    #employer_team = EmployerSerializer(many=False)

    class Meta:
        model = Bid        
        fields=["employer_team","bid_value","last_modified_date"]
        extra_kwargs  ={
           'last_modified_date':{'read_only': True}
           # "employer":{"read_only":"True"}
        } 

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ["id"]

class BidAcceptDetailSerializer(serializers.ModelSerializer):

    employer_detail = AccountSerializer(many=False)

    
    class Meta:
        model = Bid        
        fields=["bid_id","employer_detail","employer_team","bid_value","offer_accepted","offer_rolled","last_modified_date","bid_stage"]
        extra_kwargs  ={
           'last_modified_date':{'read_only': True}
           # "employer":{"read_only":"True"}
        } 


class CandidateAuctionSerializer(serializers.ModelSerializer):
    bid_details = BidDetailSerializer(many=True)
    # candidate = CandidateSerializer(many=False)
    class Meta:
        model = Auction
        fields = ["auction_id","created_date","auction_end_date","auction_live_date","base_bid","increment_amount","latest_bid","candidate_profile","bid_details"]


class UserViewSerlizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']


class CandidateAuctionViewSerializer(serializers.ModelSerializer):
    candidate_profile = CandidateProfileSerializer(many=False)
    recruiter = UserViewSerlizer(many=False)
    class Meta:
        model = Auction
        fields = ["auction_id","auction_stage","created_date","auction_end_date","auction_live_date","base_bid","increment_amount","latest_bid","candidate_profile","recruiter"]