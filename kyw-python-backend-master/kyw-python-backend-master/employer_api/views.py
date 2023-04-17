# from multiprocessing import AuthenticationError
# from re import X
from ast import Return
from urllib import response
from .models import Candidate
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import *
import jwt, datetime
from calendar import timegm
from django.core.mail import send_mail
from decouple import config
from django.contrib.auth.hashers import check_password, make_password
from django.template.loader import render_to_string
from django.template import Context
from django.core.mail import send_mail
from django.conf import settings
import configparser
from kyw_api_project import utils
from django.core.mail import EmailMessage
# import os
import logging
import traceback
import rootpath

configur = configparser.ConfigParser()
configur.read(rootpath.get_project_root() + '/kyw_api_project/config.ini')
logger = logging.getLogger('main')
# Create your views here.


class EmployerTeamView(APIView):

    def post(self, request, *args, **kwargs):

        response = Response()
        payload, response = utils.validate_token(self, request, response)
        try:
            

            if payload['userType'] == 'E':
                user = Contact.objects.filter(id=payload['member_id']).first()
                if user.role == 'Admin' and user.email_verified:

                    data = {"member_email": request.data['member_email']}

                    for i in range(len(data['member_email'])):
                        payload = {
                            'email': data['member_email'][i],
                            'userType': 'E',
                            'iat': datetime.datetime.utcnow(),
                            'id': user.account.id,
                            'role': 'Team Member',
                        }
                        token = jwt.encode(payload, config('JWT_SECRET'), algorithm='HS256')

                        send_registration_email(data['member_email'][i], token)
                    return Response({"message": "Registration Invite sent to everyone. "})
                elif user.role == 'Team Member':
                    return Response({"message": "Not permitted to perform this operation"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({"message": "Email Not Verified"})
        except(BaseException, Exception) as e:
            var = "Error || Failure in EmployerTeamView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)       
     


class EmployeeAdminView(APIView):

    def get(self, request, *args, **kwargs):

        response = Response()
        payload, response = utils.validate_token(self, request, response)
        try:
            
            if payload['userType'] == 'E':
                user = Contact.objects.using('salesforce').filter(account=payload['id']).exclude(id=payload['member_id'])
                serializer = EmployerAdminSerializer(user, many=True)

                return Response(serializer.data)
        except(BaseException, Exception) as e:
            var = "Error || Failure in EmployeeAdminView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):

        response = Response()
        payload, response = utils.validate_token(self, request, response)
        try:
            
            id = request.data['id']
            flag = request.data['flag']
            email = []
            if payload['userType'] == 'E':
                user = Contact.objects.using('salesforce').get(id=payload['member_id'])
                admin_name = user.first_name
                email.append(user.email)
                if user.role == 'Admin':
                    contactObj = Contact.objects.get(id=id)
                    email.append(contactObj.email)
                    if contactObj.role == 'Team Member':

                        employee_name = contactObj.first_name
                        if flag == False:
                            if contactObj.status == 'Active':
                                contactObj.status = "Inactive"
                                contactObj.save()
                                send_employee_status_email(email, contactObj.status, admin_name, employee_name)
                                return Response({"message": "Done"})
                            else:
                                return Response({"message": "Profile Already Inactive"})
                        if flag == True:
                            if contactObj.status == 'Inactive':
                                contactObj.status = "Active"
                                contactObj.save()
                                send_employee_status_email(email, contactObj.status, admin_name, employee_name)
                                return Response({"message": "Done"})
                            else:
                                return Response({"message": "Profile Already Active"})

                    else:
                        return Response({"message": "You cannot disable admin profile"})

                else:
                    return Response({"message": "User not authorized to perform this action"})
        except(BaseException, Exception) as e:
            var = "Error || Failure in EmployeeAdminView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NotificationView(APIView):

    def get(self, request):
        response = Response()
        payload, response = utils.validate_token(self, request, response)
        try:        
            if payload['userType']=='E':
                notificationObj = Notification.objects.using('salesforce').filter(employer_team=payload['member_id'], read=False)[:20]
                if notificationObj:
                    notifSerializers = NotificationGetSerializer(notificationObj, many = True)
                    response.data = notifSerializers.data
                    return response
                else:
                    emptyarr = []
                    response.data = emptyarr
                    return response
            else:
                return Response({"Error": "This User is not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        except(BaseException, Exception) as e:
            var = "Error || Failure in AuctionView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request, *args, **kwargs):
        response = Response()
        payload, response = utils.validate_token(self, request, response)
        try:        
            if payload['userType']=='E':
                notificationObj = Notification.objects.using('salesforce').filter(employer_team=payload['member_id'], read=False)
                if notificationObj:
                    notificationObj.update(read=True)
                    return Response({"message":"Notifcations Mark All"})
                else:
                    return Response({"message":"No New Notification to mark read"})
                    
            else:
                return Response({"Error": "This User is not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        except(BaseException, Exception) as e:
            var = "Error || Failure in NotificationView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    
def send_employee_status_email(email, status, admin_name, employee_name):
    subject = f'Profile Turned {status}'
    message = f'Admin : {admin_name}  has change profile status of {employee_name} to {status} stage'
    email_from = configur['emailDetails']['emailfrom']
    recipient_list = email
    send_mail(subject, message, email_from, recipient_list)
    return True

def send_registration_email(email, token):
    subject = 'KYW - Welcome: Verify Your Email'
    message = config('DOMAIN') + f'/api/auth/register/{token}/'
    email_from = configur['emailDetails']['emailfrom']
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
