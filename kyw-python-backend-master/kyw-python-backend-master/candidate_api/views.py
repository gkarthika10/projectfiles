from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CandidateProfileSerializer,CandidateSerializer,CandidateAuctionSerializer,BidDetailSerializer,BidAcceptDetailSerializer,CandidateAuctionViewSerializer
from .models import CandidateProfile,Candidate,Auction,Bid
from kyw_api_project import utils
from rest_framework.exceptions import *
import json
import traceback
import logging
import traceback
from django.db.models import Q
logger = logging.getLogger('main')

class CandidateProfileView(APIView):


    def put(self, request, *args, **kwargs):
        response=Response()
        payload,response=utils.validate_token(self,request,response)
        try:
            
            if payload["userType"]=='C':
                profileObj = CandidateProfile.objects.using('salesforce').filter(candidate=payload['id']).first()
                if profileObj:
                  
                    serializers=CandidateProfileSerializer(profileObj,data=request.data)
                    serializers.is_valid(raise_exception=True)
                    serializers.save()
                    return Response({"message":"Profile updated successfully"})
                else:
                    return Response({"message":"Kindly  updated your Profile "})
            else:
                return Response({"Error": "This User is not authorized to perform this action."},status=status.HTTP_401_UNAUTHORIZED)

        except(BaseException, Exception) as e:
            var = "Error || Failure in CandidateProfileView  || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        


    def post(self, request, *args, **kwargs):

        response=Response()
        payload,response=utils.validate_token(self,request,response)

        try:
            
            if payload['userType']=='C':
                candidateObj=Candidate.objects.filter(id=payload['id'])
                profileObj=CandidateProfile.objects.using('salesforce').filter(candidate=payload['id']).first()
                if profileObj:
                    return Response({"Error":"Profile Already Exists"},status=status.HTTP_409_CONFLICT)

                else:
                    try:

                        candidateObj.update(screening_stages='Profile Created')
                        profileObj=CandidateProfile.objects.using('salesforce').filter(candidate=payload['id']).first()
                        profile  = CandidateProfileSerializer(profileObj,data=request.data)
                        profile.is_valid(raise_exception=True)
                        profile.save()

                        return Response({'message': 'Profile saved successfully'})
                    except :
                        candidateObj.update(screening_stages='Email Verified')
                        logger.warning("WARNING ||  Create Candidate profile  failed   || \n")
                        return Response({'Error': "Submission Falied Kindly Try Again"},status=status.HTTP_408_REQUEST_TIMEOUT)

        except(BaseException, Exception) as e:
            var = "Error || Failure in  CandidateProfileView   || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def get(self, request, *args, **kwargs):

        response=Response()
        payload,response=utils.validate_token(self,request,response)

        try:

            if payload['userType']=='C':


                profile = CandidateProfile.objects.using('salesforce').filter(candidate=payload['id']).first()

                if profile:
                    serializers=CandidateProfileSerializer(profile)
                    return Response(serializers.data)
                else:
                    return Response({"message": "Kindly Enter Profile Details"},status=status.HTTP_200_OK)

            
            else:
                logger.error("Error || Not Valid User To get Profile Information || \n" )
                return Response({"Error": "This User is not authorized to perform this action."},status=status.HTTP_403_FORBIDDEN)
        
        except(BaseException, Exception) as e:
            var = "Error || Failure in  CandidateProfileView   || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CandidateAuctionView(APIView):
    def get(self, request, *args, **kwargs):

        response=Response()
        payload,response=utils.validate_token(self,request,response)

        try:

            

            if payload['userType']=='C':
                candidateProfileObj=CandidateProfile.objects.using('salesforce').filter(candidate=payload['id'])
                record_id=candidateProfileObj[0].record_id
                auctionObj = Auction.objects.using('salesforce').filter(candidate_profile=record_id).exclude(Q(auction_stage='Auction Finalized') | Q(auction_stage='Auction Failed') | Q(auction_stage='Candidate Hired'))
                if auctionObj:
                    serializers =CandidateAuctionViewSerializer(auctionObj, many=True)
                    return Response(serializers.data)
                else:
                    data=[]
                    return Response(data)
        except(BaseException, Exception) as e:
            var = "Error || Failure in CandidateAuctionView  || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class CandidateAcceptOffer(APIView):

    def get(self, request, *args, **kwargs):

        response=Response()
        payload,response=utils.validate_token(self,request,response)

        try:
            
            if payload['userType']  == 'C':
                candidateProfileObj=CandidateProfile.objects.using('salesforce').filter(candidate=payload['id'])
                record_id=candidateProfileObj[0].record_id
                auctionObj = Auction.objects.using('salesforce').values_list("auction_id", flat=True).filter(candidate_profile=record_id,auction_stage='Vetting')
                result = []

                for i in auctionObj:
                        bidObj= Bid.objects.using('salesforce').filter(auction=i,offer_rolled="Yes")
                        if bidObj:
                            bidSerializer =BidAcceptDetailSerializer(bidObj,many=True)
                            return Response(bidSerializer.data)
                        else:
                            return Response(result)
                return Response(result)
            else:
                return Response({"Error": "This User is not authorized to perform this action."},status=status.HTTP_403_FORBIDDEN)

        except(BaseException, Exception) as e:
            var = "Error || Failure in CandidateAcceptOffer  || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    


    def post(self, request, *args, **kwargs):

        response=Response()
        payload,response=utils.validate_token(self,request,response)

        try:
            if payload['userType']=='C':
                id=request.data['bid_id']
                bidObj=Bid.objects.using('salesforce').get(bid_id=id)
                if bidObj.bid_stage ==  "Interview" and bidObj.offer_rolled == "Yes":

                    if request.data['offer_accepted'] == True:
                        bidObj.offer_accepted="Yes"
                        bidObj.save(update_fields=["offer_accepted"])
                        return Response({"Output": "Accepted"})
                    else:
                        bidObj.offer_accepted="No"
                        bidObj.remarks_by_candidate = request.data['remark']
                        bidObj.save(update_fields=["offer_accepted","remarks_by_candidate"])

                        return Response({"Output": "Rejected"})
                else:
                    return Response({"Error": "The Candidate is no longer in Interview stage"})

                
            else:
                return Response({"Error": "This User is not authorized to perform this action."})
    
        except(BaseException, Exception) as e:
            var = "Error || Failure in Failure in CandidateAcceptOffer   || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CandidateAvailabilityView(APIView):
    def post(self, request, *args, **kwargs):
        response=Response()
        payload,response=utils.validate_token(self,request,response)
        try:

            if payload['userType']=='C':
                candidateProfileObj=CandidateProfile.objects.using('salesforce').filter(candidate=payload['id'])

                if candidateProfileObj:

                    record_id=candidateProfileObj[0].record_id
                    auctionObj = Auction.objects.using('salesforce').filter(candidate_profile=record_id).exclude(Q(auction_stage='Auction Finalized') | Q(auction_stage='Auction Failed'))

                    if auctionObj:
                        return Response({"Error": "Can not Request for Another Auctions"},status=status.HTTP_403_FORBIDDEN)
                    
                    else:
                        if candidateProfileObj[0].auction_availability == True:
                            return Response({"message": "Your Request is Being Processed Kindly Wait"})
                        else:
                            candidateProfileObj.update(auction_availability = True)
                            return Response({"message":"Your Request for auction is being proccess ,Someone from kyw with connect with you shortly"})  
                
                else:
                    return Response({"Error": "Kindly create a profile before opting for Auction"},status=status.HTTP_403_FORBIDDEN)

            else:
                return Response({"Error": "This User is not authorized to perform this action."},status=status.HTTP_403_FORBIDDEN)

        except(BaseException, Exception) as e:
            var = "Error || Failure in Failure in CandidateAcceptOffer   || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

