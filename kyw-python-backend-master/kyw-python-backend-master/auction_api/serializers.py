from dataclasses import field, fields
from rest_framework import serializers


from .models import Bid,Auction,CandidateProfile, Contact, Account,Favourite,Candidate
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["name"]
    
class EmployerSerializer(serializers.ModelSerializer):
    account = AccountSerializer(many=False) 
    class Meta:
        model = Contact
        fields = ["email","account"]  #Employer Name, Team Member Name

class CandidateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateProfile
        fields = ["first_name","last_name","cand_id","current_role","relevant_experience","notice_period","skills","current_employer",]


class CandidateProfileViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateProfile
        fields = ["first_name","last_name","cand_id","current_role","relevant_experience","notice_period","skills","current_employer","preferred_work_location"]

class BidSerializer(serializers.ModelSerializer):

    def validate(self, data):
        id=data['auction'].id
        auctionObj = Auction.objects.using('salesforce').get(id=id)
        if auctionObj.latest_bid  :
            if auctionObj.latest_bid >=data['bid_value']:
                raise serializers.ValidationError("Cannot bid lower value than current bid_value")
            return data
        else:
            if auctionObj.base_bid > data['bid_value']:
                raise serializers.ValidationError("Cannot bid lower value than current bid_value")
            return data

    class Meta:
        model = Bid        
        fields=["auction","employer_team","employer_detail","bid_value","last_modified_date"]
        extra_kwargs  ={
           'last_modified_date':{'read_only': True}
           # "employer":{"read_only":"True"}
        } 

class BidDetailSerializer(serializers.ModelSerializer):
    employer_team = EmployerSerializer(many=False)

    class Meta:
        model = Bid        
        fields=["employer_team","bid_value","last_modified_date"]
        extra_kwargs  ={
           'last_modified_date':{'read_only': True}
           # "employer":{"read_only":"True"}
        } 

class CandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateProfile
        fields=['first_name','last_name','current_role','relevant_experience',"current_employer", "cand_id"]

#class CandidatesSerializer(serializers.ModelSerializer):

#    class Meta:
#        model = Candidate
#        fields = [
#            "record_id","first_name","last_name","email","phone","email_verification","screening_stages","created_date"
#        ]



class AuctionCreateSerializer(serializers.ModelSerializer):
    #candidate_profile= CandidateSerializer(many=False)

    class Meta:
        model = Auction
        fields = ["auction_id","auction_stage","auction_end_date","auction_live_date","base_bid","increment_amount","latest_bid","cand_id","candidate_profile"]



class AuctionSerializer(serializers.ModelSerializer):
    candidate_profile= CandidateSerializer(many=False)

    class Meta:
        model = Auction
        fields = ["auction_id","created_date","auction_stage","auction_end_date","auction_live_date","base_bid","increment_amount","latest_bid","candidate_profile"]



class AuctionViewSerializer(serializers.ModelSerializer):
    candidate_profile= CandidateProfileViewSerializer(many=False)
    class Meta:
        model = Auction
        fields = ["auction_id","created_date","auction_stage","auction_end_date","auction_live_date","base_bid","increment_amount","latest_bid","candidate_profile"]

class EmployerBidDetailSerializer(serializers.ModelSerializer):
    employer_team =EmployerSerializer(many=False)
    class Meta:
        model = Bid        
        fields=["bid_id","employer_detail","employer_team","bid_value","offer_accepted","offer_rolled","last_modified_date","bid_stage"]
        extra_kwargs  ={
           'last_modified_date':{'read_only': True}
           # "employer":{"read_only":"True"}
        } 

class EmployerOfferSerializer(serializers.ModelSerializer):
    bid_details = EmployerBidDetailSerializer(many=True)
    # candidate = CandidateSerializer(many=False)
    candidate_profile = CandidateProfileSerializer(many=False)

    class Meta:
        model = Auction
        fields = ["auction_id","created_date","auction_end_date","auction_live_date","base_bid","increment_amount","latest_bid","candidate_profile","bid_details"]



class CandidateAuctionSerializer(serializers.ModelSerializer):
    bid_details = BidDetailSerializer(many=True)
    # candidate = CandidateSerializer(many=False)
    candidate_profile = CandidateProfileSerializer(many=False)

    class Meta:
        model = Auction
        fields = ["auction_id","created_date","auction_stage","auction_end_date","auction_live_date","base_bid","increment_amount","latest_bid","candidate_profile","bid_details"]
        #fields = ["auction_id","auction_end_date","auction_live_date","base_bid","increment_amount","latest_bid","bid_details"]



#class CandidateAuctionSerializer2(serializers.ModelSerializer):
#    bid_details = BidDetailSerializer(many=True)
#    candidate = CandidatesSerializer(many=False)
#    candidate_profile = CandidateProfileSerializer(many=False)

#    class Meta:
#        model = Auction
#        fields = ["auction_id","created_date","auction_end_date","auction_live_date","base_bid","increment_amount","latest_bid","candidate","candidate_profile","bid_details"]
#        #fields = ["auction_id","auction_end_date","auction_live_date","base_bid","increment_amount","latest_bid","bid_details"]







class FavouriteAuctionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ["employer_details","auction"]
class FavouriteAuctionGetSerializer(serializers.ModelSerializer):
    auction = AuctionSerializer(many=False)
    class Meta:
        model = Favourite
        fields = ["auction"]
