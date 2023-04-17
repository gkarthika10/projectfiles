from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from auction_api.models import *
from usermanagement_api.models import Candidate, CandidateProfile, Contact, Account
from .serializers import AccountsSerializer, CandProfileSerializer, CandidatesSerializer, EmpListSerializer, OpsTeamCreateSerializer, OpsTeamSerializer, RecruiterSerializer, SRCommentCreateSerializer, SRCommentSerializer, SRCreateSerializer, SRSerializer
from auction_api.serializers import *
from .models import OpsTeam, OpsTeamRole, SR_comments, ServiceRq, DashboardCache
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.exceptions import *
import jwt, datetime
import os
import logging
import traceback
from kyw_api_project import utils
import json
from django.db.models import Count
import configparser
from datetime import date
from django.utils.formats import date_format

import rootpath


configur = configparser.ConfigParser()
configur.read(rootpath.get_project_root() + '/kyw_api_project/config.ini')
logger = logging.getLogger('main')



#Start of API Classes
class ServiceRqView(APIView):

    def get(self, request, *args, **kwargs):
        response = Response()
        #payload,response = utils.validate_token(self, request, response)
        payload = request.data
        try:

#All SRs with a certain status

            if request.GET['userType']=='All' and request.GET['fetchAll'] == "false":
                rqStatus = request.GET['status']
                #servrqObj = ServiceRq.objects.using('salesforce').values_list('auction',flat=True).filter(employer_detail=request.GET['id'])
                srObjs = ServiceRq.objects.using('salesforce').filter(status=rqStatus)[:10]
                
                if srObjs:            
                    serializers=SRSerializer(srObjs,many=True)
                    response.data = serializers.data
                    return response
                    
                else:
                    res=[]
                    return Response(res)
                
            elif request.GET['userType']=='All' and request.GET['fetchAll'] == "true":
                return Response({"Err_msg":"Large Subset. Apply more filters like Status"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
## for Candidate records with a certain status
            elif request.GET['userType']=='Candidate' and request.GET['fetchAll'] == "false":
                rqStatus = request.GET['status']
                #servrqObj = ServiceRq.objects.using('salesforce').values_list('auction',flat=True).filter(employer_detail=request.GET['id'])
                srObjs = ServiceRq.objects.using('salesforce').filter(candidate=request.GET['id'],status=rqStatus)
                
                if srObjs:            
                    serializers=SRSerializer(srObjs,many=True)
                    response.data = serializers.data
                    return response
                    
                else:
                    res=[]
                    return Response(res)
                
## for Candidate records -all Statuses
            elif request.GET['userType']=='Candidate' and request.GET['fetchAll'] == "true":
                #rqStatus = request.GET['status']
                #servrqObj = ServiceRq.objects.using('salesforce').values_list('auction',flat=True).filter(employer_detail=request.GET['id'])
                srObjs = ServiceRq.objects.using('salesforce').filter(candidate=request.GET['id'])
                
                if srObjs:            
                    serializers=SRSerializer(srObjs,many=True)
                    response.data = serializers.data
                    return response
                    
                else:
                    res=[]
                    return Response(res)

## for Recruiter records with a certain status
            if request.GET['userType']=='Recruiter' and request.GET['fetchAll'] == "false":
                rqStatus = request.GET['status']
                #servrqObj = ServiceRq.objects.using('salesforce').values_list('auction',flat=True).filter(employer_detail=request.GET['id'])
                srObjs = ServiceRq.objects.using('salesforce').filter(recruiter=request.GET['id'],status=rqStatus)
                
                if srObjs:            
                    serializers=SRSerializer(srObjs,many=True)
                    response.data = serializers.data
                    return response
                    
                else:
                    res=[]
                    return Response(res)
                
## for Recruiter records -all Statuses
            elif request.GET['userType']=='Recruiter' and request.GET['fetchAll'] == "true":
                #rqStatus = request.GET['status']
                #servrqObj = ServiceRq.objects.using('salesforce').values_list('auction',flat=True).filter(employer_detail=request.GET['id'])
                srObjs = ServiceRq.objects.using('salesforce').filter(recruiter=request.GET['id'])
                
                if srObjs:            
                    serializers=SRSerializer(srObjs,many=True)
                    response.data = serializers.data
                    return response
                    
                else:
                    res=[]
                    return Response(res)

## for Auction records with a certain status
            elif request.GET['userType']=='Auction' and request.GET['fetchAll'] == "false":
                rqStatus = request.GET['status']
                #servrqObj = ServiceRq.objects.using('salesforce').values_list('auction',flat=True).filter(employer_detail=request.GET['id'])
                srObjs = ServiceRq.objects.using('salesforce').filter(auction=request.GET['id'],status=rqStatus)
                
                if srObjs:            
                    serializers=SRSerializer(srObjs,many=True)
                    response.data = serializers.data
                    return response
                    
                else:
                    res=[]
                    return Response(res)
                
## for Auction records -all Statuses
            elif request.GET['userType']=='Auction' and request.GET['fetchAll'] == "true":
                #rqStatus = request.GET['status']
                #servrqObj = ServiceRq.objects.using('salesforce').values_list('auction',flat=True).filter(employer_detail=request.GET['id'])
                srObjs = ServiceRq.objects.using('salesforce').filter(auction=request.GET['id'])
                
                if srObjs:            
                    serializers=SRSerializer(srObjs,many=True)
                    response.data = serializers.data
                    return response
                    
                else:
                    res=[]
                    return Response(res)
                
## for OpsTeam records with a certain status
            elif request.GET['userType']=='OpsTeam' and request.GET['fetchAll'] == "false":
                rqStatus = request.GET['status']
                #servrqObj = ServiceRq.objects.using('salesforce').values_list('auction',flat=True).filter(employer_detail=request.GET['id'])
                srObjs = ServiceRq.objects.using('salesforce').filter(opsteam=request.GET['id'],status=rqStatus)
                
                if srObjs:            
                    serializers=SRSerializer(srObjs,many=True)
                    response.data = serializers.data
                    return response
                    
                else:
                    res=[]
                    return Response(res)
                
## for OpsTeam records -all Statuses
            elif request.GET['userType']=='OpsTeam' and request.GET['fetchAll'] == "true":
                #rqStatus = request.GET['status']
                #servrqObj = ServiceRq.objects.using('salesforce').values_list('auction',flat=True).filter(employer_detail=request.GET['id'])
                srObjs = ServiceRq.objects.using('salesforce').filter(opsteam=request.GET['id'])
                
                if srObjs:            
                    serializers=SRSerializer(srObjs,many=True)
                    response.data = serializers.data
                    return response
                    
                else:
                    res=[]
                    return Response(res)
      
            else:
                return Response({"Err_msg": "This User is not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
 
        except(BaseException, Exception) as e:
            var = "Error || Failure in SRView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request", "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request, *args, **kwargs):
        try: 
            serializer = SRCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            #return Response(serializer.data)
            #return (data)
            response = Response()
            response.data = {
                'message' : "success"
                }
            return response
        except(BaseException, Exception) as e:
            var = "Error || Failure in SR create || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request","Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ServiceRqByRqId(APIView):
    def get(self, request, rqid, *args, **kwargs):
        response=Response()
        #payload,response=utils.validate_token(self,request,response)
        #payload=request.data
        try:
            #param = request.data['key']
            srObjs = ServiceRq.objects.using('salesforce').filter(rq_id=rqid)
                
            if srObjs:            
                serializers=SRSerializer(srObjs,many=True)
                response.data = serializers.data
                return response
                    
            else:
                res=[]
                return Response(res)


        except(BaseException, Exception) as e:
            var = "Error || Failure in Service Request by RqId  || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request", "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ServiceRqById(APIView):
    def get(self, request, srid, *args, **kwargs):
        response=Response()
        #payload,response=utils.validate_token(self,request,response)
        #payload=request.data
        try:
            #param = request.data['key']
            srObjs = ServiceRq.objects.using('salesforce').filter(record_id=srid)
                
            if srObjs:            
                serializers=SRSerializer(srObjs,many=True)
                response.data = serializers.data
                return response
                    
            else:
                res=[]
                return Response(res)


        except(BaseException, Exception) as e:
            var = "Error || Failure in Service Request by Id  || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request", "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, srid, *args, **kwargs):
        response=Response()
        #payload,response=utils.validate_token(self,request,response)
        payload=request.data
        try:

            if payload.get('status') is not None:
                profileObj = ServiceRq.objects.using('salesforce').filter(record_id=srid).update(status = payload['status'])
                if profileObj:
                    
                    return Response({"message":"SR updated successfully"})
                else:
                    return Response({"message":"SR not found"})
                
            elif payload.get('detailed_notes') is not None:
                profileObj = ServiceRq.objects.using('salesforce').filter(record_id=srid).update(detailed_notes = payload['detailed_notes'])
                if profileObj:

                    return Response({"message":"SR updated successfully"})
                else:
                    return Response({"message":"SR not found"})
                
            elif payload.get('priority') is not None:
                profileObj = ServiceRq.objects.using('salesforce').filter(record_id=srid).update(priority = payload['priority'])
                if profileObj:

                    return Response({"message":"SR updated successfully"})
                else:
                    return Response({"message":"SR not found"})
                
            elif payload.get('short_desc') is not None:
                profileObj = ServiceRq.objects.using('salesforce').filter(record_id=srid).update(short_desc = payload['short_desc'])
                if profileObj:

                    return Response({"message":"SR updated successfully"})
                else:
                    return Response({"message":"SR not found"})

            elif payload.get('opsteam') is not None:
                profileObj = ServiceRq.objects.using('salesforce').filter(record_id=srid).update(opsteam = payload['opsteam'])
                if profileObj:

                    return Response({"message":"SR updated successfully"})
                else:
                    return Response({"message":"SR not found"})
                
            elif payload.get('auction') is not None:
                profileObj = ServiceRq.objects.using('salesforce').filter(record_id=srid).update(auction = payload['auction'])
                if profileObj:

                    return Response({"message":"SR updated successfully"})
                else:
                    return Response({"message":"SR not found"})


            else:
                return Response({"message":"Invalid Update"}, status=status.HTTP_404_NOT_FOUND)


        except(BaseException, Exception) as e:
            var = "Error || Failure in SR update  || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request", "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SRComments(APIView):

    def get(self, request, *args, **kwargs):
        response = Response()
        try:
            commentObjs = SR_comments.objects.using('salesforce').filter(service_rq=request.GET['id'])
            #commentObjs = SR_comments.objects.using('salesforce')
            if commentObjs:            
                serializers=SRCommentSerializer(commentObjs,many=True)
                response.data = serializers.data
                return response
                    
            else:
                res=[]
                return Response(res)
        except(BaseException, Exception) as e:
            var = "Error || Failure in SearchComments || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request","Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try: 
            serializer = SRCommentCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            #return Response(serializer.data)
            #return (data)
            response = Response()
            response.data = {
                'message' : "success"
                }
            return response
        except(BaseException, Exception) as e:
            var = "Error || Failure in Comment Post || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request","Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        try: 
            if request.data.get('role') is not None:
                roleVal = request.data['role']
            else:
                roleVal = 'User'
            opsRoleObj =  OpsTeamRole.objects.filter(name=roleVal).first()
            #print(request.data['role'])
            #data = request.data.append()
            #data = opsRoleObj.name
            #print (opsRoleObj.id)
            data = {
                
                    "first_name":request.data['first_name'],
                    "last_name":request.data['last_name'],
                    "email":request.data['email'],
                    "password":request.data['password'],
                    "OpsRole":  opsRoleObj.id
                    }
            serializer = OpsTeamCreateSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            #return Response(serializer.data)
            #return (data)
            response = Response()
            response.data = {
                "message" : "success",
                "first_name":request.data['first_name'],
                "last_name":request.data['last_name']  }
            return response
        except(BaseException, Exception) as e:
            var = "Error || Failure in Registration || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request","Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):

        try:
            email = request.data['email']
            password = request.data['password']

            user = OpsTeam.objects.using('salesforce').filter(email=email).first()
            #user_id = user.record_id


            if user is None:
                var2 = "User not found!"
                user_id =""
                raise AuthenticationFailed(var2)
            
            else:
                user_id = user.record_id

                if user.approved == False:
                    var2 = "User not Approved yet!"
                    raise AuthenticationFailed(var2)

                if user.active == False:
                    var2 = "User not Active!"
                    raise AuthenticationFailed(var2)

                if not check_password(password, user.password):
                    var2 = "Incorrect password!"
                    raise AuthenticationFailed(var2)

                payload = {
                    'id': user.first_name,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                }

                token = jwt.encode(payload, 'secret', algorithm='HS256')
                response = Response()
                response.set_cookie(key='jwt', value=token, httponly=True)
                response.data = {
                    'message' : "success",
                    'name' : user.first_name,
                    'ops-id' : user.ops_id,
                    'id' : user_id,
                    'role': user.OpsRole.name
                    }
                return response
        
        except(BaseException, Exception) as e:
            var = "Error || Failure in Login || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"ops_id": user_id,"Err_msg":var2,"Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class UserView(APIView):

    def get(self, request):

        try:
        #    token = request.COOKIES.get('jwt')

        #    if not token:
        #        raise AuthenticationFailed('Unauthenticated!')

        #    try:
        #        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        #    except jwt.ExpiredSignatureError:
        #        raise AuthenticationFailed('Unauthenticated!')
            #print(request.GET['id'])
            user = OpsTeam.objects.using('salesforce').get(record_id = request.GET['id'])
            #print(user.OpsRole)
            print(user.first_name)
            serializer = OpsTeamSerializer(user)
            return Response(serializer.data)
        
        except(BaseException, Exception) as e:
            var = "Error || Failure in UserView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request","Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    def post(self, request):
        try:
            response = Response()
            response.delete_cookie('jwt')
            response.data = {
                'message': 'success'
            }
            return response
        except(BaseException, Exception) as e:
            var = "Error || Failure in Logout || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request","Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Recruiters(APIView):

    def get(self, request, *args, **kwargs):
        response = Response()
        try:
            if request.GET['key'] == 'first_name':
                recruiters= Contact.objects.using('salesforce').filter(first_name=request.GET['value'])
                serializers=RecruiterSerializer(recruiters,many=True)
                response.data =serializers.data
                return response
            elif request.GET['key'] == 'last_name':
                recruiters= Contact.objects.using('salesforce').filter(last_name=request.GET['value'])
                serializers=RecruiterSerializer(recruiters,many=True)
                response.data =serializers.data
                return response
            elif request.GET['key'] == 'email':
                recruiters= Contact.objects.using('salesforce').filter(email=request.GET['value'])
                serializers=RecruiterSerializer(recruiters,many=True)
                response.data =serializers.data
                return response
            elif request.GET['key'] == 'phone':
                recruiters= Contact.objects.using('salesforce').filter(mobile_phone=request.GET['value'])
                serializers=RecruiterSerializer(recruiters,many=True)
                response.data =serializers.data
                return response
            else:
                return Response({"Err_msg":"could not process the request","Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
                
        except(BaseException, Exception) as e:
            var = "Error || Failure in SearchRecruiter || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request","Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class Companies(APIView):
    def get(self, request, *args, **kwargs):
        response = Response()
        try:
            if request.GET['key'] == 'name':
                companies= Account.objects.using('salesforce').filter(name=request.GET['value'])
                serializers=AccountsSerializer(companies,many=True)
                response.data =serializers.data
                return response
            elif request.GET['key'] == 'website':
                companies= Account.objects.using('salesforce').filter(website=request.GET['value'])
                serializers=AccountsSerializer(companies,many=True)
                response.data =serializers.data
                return response
            else:
                return Response({"Err_msg":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
                
        except(BaseException, Exception) as e:
            var = "Error || Failure in SearchCompanies || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request","Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class Employees(APIView):
    def get(self, request, keyid, *args, **kwargs):


        try:
            if keyid is None:

                return Response({"Err_msg":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

            else:    

                recruiters= Contact.objects.using('salesforce').filter(account_id=keyid)
                response = Response()
                #response.data = {
                #'message': keyid
                #}
                #return response
                serializers=EmpListSerializer(recruiters,many=True)
                response.data =serializers.data
                return response
            
        except(BaseException, Exception) as e:
            var = "Error || Failure in ListEmployees || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request","Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Candidates(APIView):

    def get(self, request, *args, **kwargs):
        response = Response()
        try:
            if request.GET['key'] == 'first_name':
                candidates= Candidate.objects.using('salesforce').filter(first_name=request.GET['value'])
                serializers=CandidatesSerializer(candidates,many=True)
                response.data =serializers.data
                return response
            elif request.GET['key'] == 'last_name':
                candidates= Candidate.objects.using('salesforce').filter(last_name=request.GET['value'])
                serializers=CandidatesSerializer(candidates,many=True)
                response.data =serializers.data
                return response
            elif request.GET['key'] == 'email':
                candidates= Candidate.objects.using('salesforce').filter(email=request.GET['value'])
                serializers=CandidatesSerializer(candidates,many=True)
                response.data =serializers.data
                return response
            elif request.GET['key'] == 'phone':
                print (request.GET['value'])
                candidates= Candidate.objects.using('salesforce').filter(phone=request.GET['value'])
                serializers=CandidatesSerializer(candidates,many=True)
                response.data =serializers.data
                return response
            else:
                return Response({"Err_msg":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
                
        except(BaseException, Exception) as e:
            var = "Error || Failure in SearchRecruiter || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request", "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CandProfile(APIView):
    def get(self, request, keyid, *args, **kwargs):


        try:
            if keyid is None:

                return Response({"Err_msg":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

            else:    

                candidateProfiles=CandidateProfile.objects.using('salesforce').filter(cand_id=keyid)
                #recruiters= Contact.objects.using('salesforce').filter(account_id=keyid)
                response = Response()
                #response.data = {
                #'message': keyid
                #}
                #return response
                serializers=CandProfileSerializer(candidateProfiles,many=True)
                response.data =serializers.data
                return response
            
        except(BaseException, Exception) as e:
            var = "Error || Failure in ViewCandProfile || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request", "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def put(self, request, keyid, *args, **kwargs):
        response=Response()
        #payload,response=utils.validate_token(self,request,response)
        payload=request.data
        try:
            #param = request.data['key']

            if payload.get('background_verification') is not None:
                profileObj = CandidateProfile.objects.using('salesforce').filter(cand_id=keyid).update(background_verification = payload['background_verification'])
                if profileObj:
                    
                    return Response({"message":"Profile updated successfully"})
                else:
                    return Response({"message":"Candidate not found"})
                
            elif payload.get('auction_availability') is not None:
                profileObj = CandidateProfile.objects.using('salesforce').filter(cand_id=keyid).update(auction_availability = payload['auction_availability'])
                if profileObj:

                    return Response({"message":"Profile updated successfully"})
                else:
                    return Response({"message":"Candidate not found"})
            else:
                return Response({"message":"Invalid Update"}, status=status.HTTP_404_NOT_FOUND)


        except(BaseException, Exception) as e:
            var = "Error || Failure in Candidate Profile update  || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request", "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class CandidatesById(APIView):

    def put(self, request, candid, *args, **kwargs):
        response=Response()
        #payload,response=utils.validate_token(self,request,response)
        payload=request.data
        try:
            #param = request.data['key']
            if payload.get('email_verification') is not None:
                candObj = Candidate.objects.using('salesforce').filter(record_id=candid ).update(email_verification = payload['email_verification'])
                if candObj:
                    var2 = "Profile updated successfully"
                    return Response({"message": var2})
                else:
                    var2 = "Candidate not found"
                    return Response({"message": var2}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            elif payload.get('screening_stages') is not None:
                candObj = Candidate.objects.using('salesforce').filter(record_id=candid).update(screening_stages = payload['screening_stages'])
                if candObj:
                    var2 = "Profile updated successfully"
                    return Response({"message":var2 })
                else:
                    var2 = "Candidate not found"
                    return Response({"message":var2}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                var2 = "Invalid Update"
                return Response({"message":var2 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        except(BaseException, Exception) as e:
            var = "Error || Failure in Candidate Get by Id  || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"Err_msg":var2, "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get(self, request, candid, *args, **kwargs):
        response = Response()
        try:

            candidates= Candidate.objects.using('salesforce').filter(record_id=candid)
            serializers=CandidatesSerializer(candidates,many=True)
            response.data =serializers.data
            return response
                
        except(BaseException, Exception) as e:
            var = "Error || Failure in SearchCandidatesbyId || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request", "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OpsTeamView(APIView):

    def get(self, request):

        response = Response()
        try:
            if request.GET['key'] == 'first_name':
                user= OpsTeam.objects.using('salesforce').filter(first_name=request.GET['value'])
                serializers=OpsTeamSerializer(user,many=True)
                response.data =serializers.data
                return response
            elif request.GET['key'] == 'last_name':
                user= OpsTeam.objects.using('salesforce').filter(last_name=request.GET['value'])
                serializers=OpsTeamSerializer(user,many=True)
                response.data =serializers.data
                return response
            elif request.GET['key'] == 'email':
                user= OpsTeam.objects.using('salesforce').filter(email=request.GET['value'])
                serializers=OpsTeamSerializer(user,many=True)
                response.data =serializers.data
                return response
            else:
                return Response({"Err_msg":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
                
        except(BaseException, Exception) as e:
            var = "Error || Failure in Search Ops Team || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request", "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class OpsTeamById(APIView):


    def get(self, request, opid, *args, **kwargs):
        response = Response()
        try:

            user = OpsTeam.objects.using('salesforce').get(record_id = opid)
            #print(user.OpsRole)
            #print(user.first_name)
            serializer = OpsTeamSerializer(user)
            return Response(serializer.data)
                
        except(BaseException, Exception) as e:
            var = "Error || Failure in SearchOpTeamsbyId || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request", "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def put(self, request, opid, *args, **kwargs):
        response=Response()
        #payload,response=utils.validate_token(self,request,response)
        payload=request.data
        try:
            #param = request.data['key']
            if payload.get('active') is not None:
                opsObj = OpsTeam.objects.using('salesforce').filter(record_id=opid ).update(active = payload['active'])
                if opsObj:
                    var2 = "Profile updated successfully"
                    return Response({"message": var2})
                else:
                    var2 = "Member not found"
                    return Response({"message": var2}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif payload.get('approved') is not None:
                opsObj = OpsTeam.objects.using('salesforce').filter(record_id=opid ).update(approved = payload['approved'])
                if opsObj:
                    var2 = "Profile updated successfully"
                    return Response({"message": var2})
                else:
                    var2 = "Member not found"
                    return Response({"message": var2}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                var2 = "Invalid Update"
                return Response({"message": var2}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        except(BaseException, Exception) as e:
            var = "Error || Failure in updating Ops Team member by Id  || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"Err_msg":var2, "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RecruitersById(APIView):
    
    def get(self, request, recid, *args, **kwargs):
        response = Response()
        try:
            recruiters= Contact.objects.using('salesforce').filter(member_id=recid)
            serializers=RecruiterSerializer(recruiters,many=True)
            response.data =serializers.data
            return response
                
        except(BaseException, Exception) as e:
            var = "Error || Failure in SearchRecruitersbyId || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request", "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, recid, *args, **kwargs):
        response=Response()
        #payload,response=utils.validate_token(self,request,response)
        payload=request.data
        try:
            #param = request.data['key']
            if payload.get('role') is not None:
                candObj = Contact.objects.using('salesforce').filter(member_id=recid ).update(role = payload['role'])
                if candObj:
                    return Response({"message":"Recruiter updated successfully"})
                else:
                    var2 = "Recruiter not found"
                    return Response({"message": var2},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            elif payload.get('email_verification') is not None:
                candObj = Contact.objects.using('salesforce').filter(member_id=recid ).update(email_verified = payload['email_verification'])
                if candObj:
                    return Response({"message":"Recruiter updated successfully"})
                else:
                    var2 = "Recruiter not found"
                    return Response({"message": var2}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                    var2 = "Update not allowed"
                    return Response({"message": var2}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except(BaseException, Exception) as e:
            var = "Error || Failure in updateRecruiterById || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":var2, "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CompaniesById(APIView):
    
    def get(self, request, compid, *args, **kwargs):
        response = Response()
        try:
            companies= Account.objects.using('salesforce').filter(employer_details_id=compid)
            serializers=AccountsSerializer(companies,many=True)
            response.data =serializers.data
            return response
                
        except(BaseException, Exception) as e:
            var = "Error || Failure in SearchCompaniesbyId || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request", "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, compid, *args, **kwargs):
        response=Response()
        #payload,response=utils.validate_token(self,request,response)
        payload=request.data
        try:
            #param = request.data['key']
            if payload.get('bgv') is not None:
                candObj = Account.objects.using('salesforce').filter(employer_details_id=compid ).update(bgv_completed = payload['bgv'])
                if candObj:
                    return Response({"message":"Company BGV updated successfully"})
                else:
                    var2 = "Company not found"
                    return Response({"message": var2},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                    var2 = "Update not allowed"
                    return Response({"message": var2}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except(BaseException, Exception) as e:
            var = "Error || Failure in updatecompanyById || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":var2, "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AuctionView(APIView):

    def post(self, request, *args, **kwargs):
        
        #payload,response=utils.validate_token(self,request,response)
        payload = request.data
        response=Response()
        try:
                
            #param = request.data['key']
            candObj = Candidate.objects.using('salesforce').get(record_id=payload['cand_id'])
            print (candObj.first_name)
            candProfObj =  CandidateProfile.objects.using('salesforce' ).get(cand_id= payload['cand_id'])
            print (candProfObj.last_name)
            if candObj.email_verification == True:
                if candProfObj.auction_availability == True:
                    if candProfObj.background_verification == True:
                        print("---------")
                        print ({"cand_id": payload['cand_id']})
                        print({"message":"All conditions met"})
                        print("---------")
                        #payload.append(candProfObj)
                        newAuct ={
                                #"created_date": payload['created_date'],
                                "auction_end_date": payload['auction_end_date'],
                                "auction_live_date": payload['auction_live_date'],
	                            "auction_stage": payload['auction_stage'],
                                "base_bid": payload['base_bid'],
                                "increment_amount": payload['increment_amount'],
	                            "cand_id": payload['cand_id'],
                                "candidate_profile": candProfObj.record_id
                                }
                        serializer = AuctionCreateSerializer(data=newAuct)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        print (serializer.data)
                        #aucObj = Auction.objects.using('salesforce').filter(record_id=candid ).update(email_verification = request.data['email_verification'])
                        
                        return Response(serializer.data)

                    else:
                        return Response({"err_msg":"Fail.Background verification not Complete"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"err_msg":"Fail.Auction Availability not Active"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"err_msg":"Fail.Email Verification pending for Candidate"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    
        except(BaseException, Exception) as e:
            var = "Error || Failure in Auction Post  || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request", "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def get(self, request, *args, **kwargs):
        response = Response()
        #payload,response = utils.validate_token(self, request, response)
        payload = request.data
        try:

            #aucStage = request.GET['aucStage']    
        
## for company specific records with a certain status
            if request.GET['userType']=='Company' and request.GET['fetchAll'] == "false":
                aucStage = request.GET['aucStage']
                bidObjs = Bid.objects.using('salesforce').values_list('auction',flat=True).filter(employer_detail=request.GET['id'])
                auctionObj = Auction.objects.using('salesforce').filter(auction_stage=aucStage,id__in=bidObjs)
                
                if auctionObj:            
                    serializers=AuctionSerializer(auctionObj,many=True)
                    response.data = serializers.data
                    return response
                    
                else:
                    res=[]
                    return Response(res)
                

## for company specific records with all statuses
            if request.GET['userType']=='Company' and request.GET['fetchAll'] == "true":
                #aucStage = request.GET['aucStage']
                bidObjs = Bid.objects.using('salesforce').values_list('auction',flat=True).filter(employer_detail=request.GET['id'])
                auctionObj = Auction.objects.using('salesforce').filter(id__in=bidObjs)
                
                if auctionObj:            
                    serializers=AuctionSerializer(auctionObj,many=True)
                    response.data = serializers.data
                    return response
                    
                else:
                    res=[]
                    return Response(res)


## for recruiter specific records with a certain status
            if request.GET['userType']=='Recruiter' and request.GET['fetchAll'] == "false":
                aucStage = request.GET['aucStage']
                bidObjs = Bid.objects.using('salesforce').values_list('auction',flat=True).filter(employer_team=request.GET['id'])
                auctionObj = Auction.objects.using('salesforce').filter(auction_stage=aucStage,id__in=bidObjs)
                
                if auctionObj:            
                    serializers=AuctionSerializer(auctionObj,many=True)
                    response.data = serializers.data
                    return response
                    
                else:
                    res=[]
                    return Response(res)


## for recruiter specific records with all statuses
            if request.GET['userType']=='Recruiter' and request.GET['fetchAll'] == "true":
                #aucStage = request.GET['aucStage']
                bidObjs = Bid.objects.using('salesforce').values_list('auction',flat=True).filter(employer_team=request.GET['id'])
                auctionObj = Auction.objects.using('salesforce').filter(id__in=bidObjs)
                
                if auctionObj:            
                    serializers=AuctionSerializer(auctionObj,many=True)
                    response.data = serializers.data
                    return response
                    
                else:
                    res=[]
                    return Response(res)



#fetchAll records for a Status            
            elif request.GET['userType']=='All' and request.GET['fetchAll'] == "true":
                return Response({"Err_msg":"Large Subset. Apply more filters like Status"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#fetchAll records for a Status            
            elif request.GET['userType']=='All' and request.GET['fetchAll'] == "false":
                aucStage = request.GET['aucStage']
                auctionObj = Auction.objects.using('salesforce').filter(auction_stage=aucStage)[:10]                
                
                if auctionObj:            
                    serializers=AuctionSerializer(auctionObj,many=True)
                    response.data = serializers.data
                    return response                    
                else:
                    res=[]
                    return Response(res)            

#fetchAll records for a Candidate
            elif request.GET['userType']=='Candidate' and request.GET['fetchAll'] == "true":
                #print(payload['id'])
                canAucObj = Auction.objects.using('salesforce').filter(cand_id=request.GET['id'])
                
                if canAucObj:
                    serializers=CandidateAuctionSerializer(canAucObj,many = True)
                    response.data = serializers.data
                    return response
                else:
                    res=[]
                    return Response(res)    
                
#fetchAll records for a Candidate
            elif request.GET['userType']=='Candidate' and request.GET['fetchAll'] == "false":
                #print(payload['id'])
                aucStage = request.GET['aucStage']
                canAucObj = Auction.objects.using('salesforce').filter(cand_id=request.GET['id'], auction_stage=aucStage)
                
                if canAucObj:
                    serializers=CandidateAuctionSerializer(canAucObj,many = True)
                    response.data = serializers.data
                    return response
                else:
                    res=[]
                    return Response(res)   
            
            else:
                return Response({"Err_msg": "This User is not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        
        
        
        except(BaseException, Exception) as e:
            var = "Error || Failure in AuctionView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request", "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BidView(APIView):

    def post(self, request):
        response=Response()
    #    payload,response=utils.validate_token(self,request,response)
        payload = request.data
        try:
            

            if 1==1:
                
                

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
                            return Response({"Err_msg":"Cannot bid same or lower value than current bid_value"},status=status.HTTP_406_NOT_ACCEPTABLE)   # can be change 
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
                           
                            return Response({"Err_msg":"Cannot bid lower value than current bid_value"},status=status.HTTP_400_BAD_REQUEST)
                        bids.save()
                        bidsemail = Bid.objects.filter(auction=request.data['auction_id']).exclude(employer_detail=payload['id'])

                        
                    

                        for i in bidsemail:
                            
                            notify_other.append(i.employer_team.email)
                        
                       

                        response.data = {
                            "message":"Bid Placed Successfully"
                        }
                        
                        return response
                else:
                    return Response({"Err_msg": "Auction is not Live Hence You cannot bid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            
            
            else:
                return Response({"Err_msg": "This User is not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        except(BaseException, Exception) as e:
            var = "Error || Failure in BidView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request", "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CandidateAuctionView(APIView):

    def put(self, request,id):
        response=Response()
        #payload,response=utils.validate_token(self,request,response)
        payload=request.data
        try:
            if payload.get('auction_stage') is not None:
                aucObj = Auction.objects.using('salesforce').filter(auction_id=id).update(auction_stage = payload['auction_stage'])
                if aucObj:
                    return Response({"message":"Auction updated successfully"})
                else:
                    return Response({"message":"Auction not found"})
                
            elif payload.get('auction_live_date') is not None:
                aucObj = Auction.objects.using('salesforce').filter(auction_id=id).update(auction_live_date = payload['auction_live_date'])
                if aucObj:
                    return Response({"message":"Auction updated successfully"})
                else:
                    return Response({"message":"Auction not found"})
            elif payload.get('auction_end_date') is not None:
                aucObj = Auction.objects.using('salesforce').filter(auction_id=id).update(auction_end_date = payload['auction_end_date'])
                if aucObj:
                    return Response({"message":"Auction updated successfully"})
                else:
                    return Response({"message":"Auction not found"})
            elif payload.get('manager_approval') is not None:
                aucObj = Auction.objects.using('salesforce').filter(auction_id=id).update(manager_approval = payload['manager_approval'])
                if aucObj:
                    return Response({"message":"Auction updated successfully"})
                else:
                    return Response({"message":"Auction not found"})
            else:
                return Response({"message":"Invalid Update"}, status=status.HTTP_404_NOT_FOUND)


        except(BaseException, Exception) as e:
            var = "Error || Failure in Auction update  || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request", "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def get(self, request,id):
        response=Response()
    #    payload,response=utils.validate_token(self,request,response)
        payload = request.data
        try:

            canAucObj = Auction.objects.using('salesforce').filter(auction_id=id) 
            
            if canAucObj:
                #canAucObj = Auction.objects.using('salesforce').filter(auction_id=id)
                serializers=CandidateAuctionSerializer(canAucObj, many=True)
                response.data = serializers.data
                return response
            else:
                #return Response({"Err_msg": "This User is not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
                res=[]
                return Response(res)


        except(BaseException, Exception) as e:
            var = "Error || Failure in CandidateAuctionView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request", "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class DashboardView(APIView):


    def get(self, request, *args, **kwargs):
        response = Response()
        try:
            today = date.today()
            #print (today)
            date_string = date_format(today, format= 'Y-m-d')
            #print (date_string)
            date_string_start = date_string + 'T00:00:01Z'
            date_string_end = date_string + 'T23:59:59Z'
            #print (date_string)
            
            #Candidates_Onboarded = Candidate.objects.using('salesforce').filter(created_date__range = (("2023-02-09T14:47:04Z"),("2023-02-09T14:57:04Z"))).count()
            candidates_onboarded = Candidate.objects.using('salesforce').filter(created_date__range = (date_string_start,date_string_end)).count()
            candidates_auctionReady = CandidateProfile.objects.using('salesforce').filter(auction_availability = True).count()
            recruiters_onboarded = Contact.objects.using('salesforce').filter(created_date__range = (date_string_start,date_string_end)).count()
            companies_onboarded = Account.objects.using('salesforce').filter(created_date__range = (date_string_start,date_string_end)).count()
            live_auctions = Auction.objects.using('salesforce').filter(auction_stage = 'Auction Active').count()
            draft_auctions = Auction.objects.using('salesforce').filter(auction_stage = 'Draft').count()
            managerApproval_auctions = Auction.objects.using('salesforce').filter(auction_stage = 'Manager Approval').count()
            sr_open = ServiceRq.objects.using('salesforce').filter(status="Open").count()
            sr_inprogress = ServiceRq.objects.using('salesforce').filter(status="In-progress").count()
            sr_closed = ServiceRq.objects.using('salesforce').filter(status="Closed").count()
            opsteam_count = OpsTeam.objects.using('salesforce').filter(active=True, approved=True ).count()
            cand_verify_pending = Candidate.objects.using('salesforce').filter(email_verification = False).count()
            recruiter_verify_pending = Contact.objects.using('salesforce').filter(email_verified = False).count()  
            companies_bgv_pending = Account.objects.using('salesforce').filter(bgv_completed = False).count()       

            response.data = {
                "Candidates_Onboarded": candidates_onboarded,
                "Recruiters_Onboarded" : recruiters_onboarded,
                "Companies_Onboarded" : companies_onboarded,
                "Companies_BGV_Pending" : companies_bgv_pending,
                "Candidate_Verify_Pending" : cand_verify_pending,
                "Recruiter_Verify_Pending" : recruiter_verify_pending,
                "OpsTeam_Count": opsteam_count,
                "Live_Auction": live_auctions,
                "Draft_Auctions": draft_auctions,
                "ManagerApproval_Auctions": managerApproval_auctions,
                "Candidates_AuctionReady": candidates_auctionReady,
                "SR_Open": sr_open,
                "SR_InProgress": sr_inprogress,
                "SR_Closed": sr_closed
                }
            return response

                
        except(BaseException, Exception) as e:
            var = "Error || Failure in DashboardView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Err_msg":"could not process the request", "Trace": var}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DashboardCachedView(APIView):

    def get(self, request, *args, **kwargs):
        response = Response()
        cache_data = {}
        for cache in DashboardCache.objects.all():
            cache_data[cache.name ] = cache.count 
        response.data = cache_data
        return response


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

