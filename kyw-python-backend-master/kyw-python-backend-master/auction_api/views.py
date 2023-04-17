from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from decouple import config
from decouple import config
from django.contrib.auth.hashers import check_password,make_password
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.response import Response
from rest_framework.exceptions import *
from calendar import timegm
from .models import *
from kyw_api_project import utils
import json
from django.db.models import Count
import configparser
import os
import logging
import traceback



import rootpath
# cfg_path = os.path.join(os.path.dirname(__file__), 'usrmgmt_config.ini')

configur = configparser.ConfigParser()
configur.read(rootpath.get_project_root() + '/kyw_api_project/config.ini')
logger = logging.getLogger('main')


class AuctionView(APIView):
    def get(self, request, *args, **kwargs):
        response = Response()
        payload,response = utils.validate_token(self, request, response)
        try:
            aucStage = request.headers['aucStage']
            if payload['userType']=='E':
                if aucStage =='Auction Active_R':
                    roles = Auction.objects.using('salesforce').filter(auction_stage='Auction Active').values('role').annotate(countVal=Count('candidate_profile')).values_list('role', flat=True)
                    candidateList = []
                    for role in roles:
                        candidates = Auction.objects.using('salesforce').filter(role=role,auction_stage='Auction Active')
                        auctionsDict = {}
                        auctionsDict['role'] = role
                        auctionsDict['no_of_canididates'] = candidates.__len__()
                        auctionsDict['candidate'] = json.loads(json.dumps(AuctionSerializer(candidates,many=True).data))
                        candidateList.append(auctionsDict)
                    auctionsDict = {}
                    auctionsDict['data'] = candidateList
                    response.data = auctionsDict
                    return response
                    #auctionObj = Auction.objects.using('salesforce').filter(auction_stage='Auction Active')
                elif aucStage == 'Auction Active':
                    auctionObj = Auction.objects.using('salesforce').filter(auction_stage='Auction Active')
                    serializers=AuctionViewSerializer(auctionObj,many=True)
                    response.data = serializers.data
                    return response
        
                elif aucStage == 'Auction Active_E':
                    
                    bidObjs = Bid.objects.using('salesforce').values_list('auction',flat=True).filter(employer_detail=payload['id'])

                    auctionObj = Auction.objects.using('salesforce').filter(auction_stage='Auction Active',id__in=bidObjs)
                elif aucStage == 'Vetting_E':
                    bidObjs = Bid.objects.using('salesforce').values_list('auction',flat=True).filter(employer_detail=payload['id'])
                    auctionObj = Auction.objects.using('salesforce').filter(auction_stage='Vetting',id__in=bidObjs)

                elif aucStage == 'Auction Finalized':
                    bidObjs = Bid.objects.using('salesforce').values_list('auction',flat=True).filter(employer_detail=payload['id'])
                    auctionObj = Auction.objects.using('salesforce').filter(auction_stage='Auction Finalized',id__in=bidObjs)

                else:
                    return Response({"Error":"aucStage Header not valid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                
                if auctionObj:            
                    serializers=AuctionSerializer(auctionObj,many=True)
                    response.data = serializers.data
                    return response
                    
                else:
                    res=[]
                    return Response(res)
            else:
                return Response({"Error": "This User is not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        except(BaseException, Exception) as e:
            var = "Error || Failure in AuctionView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BidView(APIView):

    def post(self, request):
        response=Response()
        payload,response=utils.validate_token(self,request,response)
        try:
            

            if payload['userType']=='E':
                
                

                if  Auction.objects.using('salesforce').get(id=request.data['auction_id']).auction_stage == "Auction Active":
                    bidObj = Bid.objects.filter(employer_detail=payload['id'],auction=request.data['auction_id'])
                      
                    
                    if bidObj:
                        notify_other =[]
                        bidsemail = Bid.objects.filter(auction=request.data['auction_id']).exclude(employer_detail = payload['id'])
                        

                        for i in bidsemail:
                            
                            notify_other.append(i.employer_team.email)

                    

                        
                        id=request.data['auction_id']
                        auctionObj = Auction.objects.using('salesforce').get(id=id)
                        if request.data['bid_value'] > auctionObj.latest_bid:
                            bidObj.update(bid_value=request.data['bid_value'])
                            memberObj=Contact.objects.get(id=payload['member_id'])
                            
                            if bidObj[0].employer_team.email != memberObj.email : 
                                bidObj.update(employer_team=memberObj)

                            

                            response.data = {
                                "message":"Bid Updated Successfully"
                            }
                            return response
                        else:
                            return Response({"Error":"Cannot bid same or lower value than current bid_value"},status=status.HTTP_406_NOT_ACCEPTABLE)   # can be change 
                    else:
                        notify_other =[]
                        #empPrflObj= EmployerProfile.objects.get(employer=payload['id'])
                        data= {
                            "employer_detail":payload['id'],
                            "bid_value": request.data['bid_value'],
                            'auction':request.data['auction_id'],
                            "employer_team":payload['member_id']
                        }
                        
                        contactObj= Contact.objects.using('salesforce').get(id=payload['member_id'])
                        
                        bids= BidSerializer(data=data)
                        try:
                            bids.is_valid(raise_exception=True)
                        except ValidationError as e :
                           
                            return Response({"Error":"Cannot bid lower value than current bid_value"},status=status.HTTP_400_BAD_REQUEST)
                        bids.save()
                        bidsemail = Bid.objects.filter(auction=request.data['auction_id']).exclude(employer_detail=payload['id'])

                        
                    

                        for i in bidsemail:
                            
                            notify_other.append(i.employer_team.email)
                        
                       

                        response.data = {
                            "message":"Bid Placed Successfully"
                        }
                        
                        return response
                else:
                    return Response({"Error": "Auction is not Live Hence You cannot bid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response({"Error": "This User is not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        except(BaseException, Exception) as e:
            var = "Error || Failure in BidView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CandidateAuctionView(APIView):

    def get(self, request,id):
        response=Response()
        payload,response=utils.validate_token(self,request,response)
        try:
            
            
            if payload['userType']=='E':
                canAucObj = Auction.objects.using('salesforce').get(auction_id=id)
                serializers=CandidateAuctionSerializer(canAucObj)
                response.data = serializers.data
                return response
            else:
                return Response({"Error": "This User is not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        except(BaseException, Exception) as e:
            var = "Error || Failure in CandidateAuctionView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployerInterviewAuctionView(APIView):

    def get(self,request):
        response=Response()
        payload,response=utils.validate_token(self,request,response)
        try:
            # aucStage = request.headers['aucStage']
            


            if payload['userType']=='E' :
                    bidObjs = Bid.objects.using('salesforce').values_list('auction',flat=True).filter(employer_detail=payload['id'],bid_stage='Interview')
                    auctionObj = Auction.objects.using('salesforce').filter(auction_stage='Vetting',id__in=bidObjs)
                    if auctionObj:            
                        serializers=AuctionSerializer(auctionObj,many=True)
                        response.data = serializers.data
                        return response
                    
                    else:
                        res=[]
                        
                        return Response(res)
            else:
                return Response({"Error": "This User is not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        except(BaseException, Exception) as e:
            var = "Error || Failure in EmployeeOfferRoll || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EmployerOfferView(APIView):

    def get(self, request,id, *args, **kwargs):
        response=Response()
        payload,response=utils.validate_token(self,request,response)
        try:
            
            
            if payload['userType']=='E':
                canAucObj = Auction.objects.using('salesforce').get(auction_id=id)
                serializers=EmployerOfferSerializer(canAucObj)
                response.data = serializers.data
                return response
            else:
                return Response({"Error": "This User is not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        except(BaseException, Exception) as e:
            var = "Error || Failure in EmployerAuctionView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self,request):
        response=Response()
        payload,response=utils.validate_token(self,request,response)
        try:
            
            
            if payload['userType']=='E':
                id=request.data['bid_id']
               
                accountObj=Account.objects.get(id=payload["id"])
               
                
                #bidObj=Bid.objects.using('salesforce').get(bid_id=id)
                bidObj=Bid.objects.using('salesforce').filter(bid_id=id)
                
                canAucObj = Auction.objects.using('salesforce').get(id=bidObj[0].auction.id)

                candidate_email=canAucObj.candidate_profile.candidate_email
                candidate_name=canAucObj.candidate_profile.first_name
                recruiter=canAucObj.recruiter.email



               

           

                if bidObj[0].bid_stage ==  "Interview":

                    if accountObj==bidObj[0].employer_detail:
                        employer=bidObj[0].employer_detail.name
                        
                        if request.data['offer_rolled']== True:
                            state = True
                            

                            bidObj.update(offer_rolled="Yes")
                            # -- mail to poc and candidate --
                          
                            email=[recruiter,candidate_email]
                            send_offer_rolled_email(email ,state,candidate_name,employer,candidate_email)
                           


                        else:
                            state =False
                            remarks_by_employer = request.data['remark']
                            bidObj.update(offer_rolled="No",remarks_by_employer=remarks_by_employer)
                            email=[recruiter]
                            send_offer_rolled_email(email ,state,candidate_name,employer,candidate_email)
                            
                            #mail to po
                            #bidObj.save()


                    return Response({"message": "Your Offer Status have been saved successfully"})


                else:
                    return Response({"Error": "This User is not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)

            else:
                return Response({"Error": "This User is not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        except(BaseException, Exception) as e:
            var = "Error || Failure in EmployerAuctionView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class FavouritesView(APIView):
    def post(self, request):
        response=Response()
        payload,response=utils.validate_token(self,request,response)
        try:
            if payload['userType']=='E':
                favObj = Favourite.objects.filter(employer_details=payload['id'],auction=request.data['auction_id'])
                if not favObj:
                    data= {
                        "employer_details":payload['id'],
                        'auction':request.data['auction_id']
                    }
                    fav = FavouriteAuctionPostSerializer(data=data)
                    fav.is_valid(raise_exception=True)
                    fav.save()
                    response.data = {"message":"Added to Favourites"}
                else:
                    response.data = {"message":"Auction already marked as Favourite"}
                return response
            else:
                return Response({"Error": "This User is not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        except(BaseException, Exception) as e:
            var = "Error || Failure in FavouritesView || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get(self, request):

        response=Response()
        payload,response=utils.validate_token(self,request,response)
        try:
           
            if payload['userType']=='E':
                favObj = Favourite.objects.filter(employer_details=payload['id'])
                fav = FavouriteAuctionGetSerializer(favObj, many=True)
                response.data = fav.data
                return response
            else:
                return Response({"Error": "This User is not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        except(BaseException, Exception) as e:
            var = "Error || Failure in FavouritesView || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        response=Response()
        payload,response=utils.validate_token(self,request,response)
        try:
            if payload['userType']=='E':
                favObj = Favourite.objects.filter(employer_details=payload['id'],auction=id)
                favObj.delete()
                response.data = {"message":"Removed from Favourites"}
                return response
        except(BaseException, Exception) as e:
            var = "Error || Failure in FavouritesView || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def send_updated_bid_mail(email):
    subject = 'KYW - Bid update '
    message = 'Hi,\n \n Your bid has been updated successfully'
    email_from = configur['emailDetails']['emailfrom']
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True  

def notify_other_bid_mail(email):
    subject = 'KYW - new Bid '
    message = 'Hi,\nThere is a new bid  on your selected candidate'
    email_from = configur['emailDetails']['emailfrom']
    recipient_list = email
    send_mail(subject, message, email_from, recipient_list)
    return True    

def send_new_bid_email(email):
    subject = 'KYW - Bid Placed'
    message = 'Hi,\nYour bid placed successfully'
    email_from = configur['emailDetails']['emailfrom']
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def send_offer_rolled_email(email ,status,candidate_name,employer,candidate_email):
    subject = f'Employer : {employer} Candidate: {candidate_name} Offer: '+('Recieved'  if  status else 'Rejected')
    message1 = f"For Candidate: {candidate_name} Employer: {employer} have rolled offer"
    message2 = f"For Candidate: {candidate_name} Employer: {employer} have rejected the application"
    message = message1  if status else message2

    email_from = configur['emailDetails']['emailfrom']
    recipient_list = email
    send_mail(subject, message, email_from, recipient_list)
    return True     

