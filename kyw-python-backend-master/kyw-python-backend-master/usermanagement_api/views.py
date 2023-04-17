# from multiprocessing import AuthenticationError
# from re import X
from ast import Return
from urllib import response
from opscentre_usermanagement_api.serializers import CandidatesSerializer
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
# cfg_path = os.path.join(os.path.dirname(__file__), 'usrmgmt_config.ini')

configur = configparser.ConfigParser()
configur.read(rootpath.get_project_root() + '/kyw_api_project/config.ini')
logger = logging.getLogger('main')
# Create your views here.

class RegisterView(APIView):
    def post(self, request):

        userType = request.headers['userType']
        if userType == 'C':
            canObj = Candidate.objects.filter(email=request.data['email'])
            if canObj:
                return Response({"Error": "Candidate with this email already exists."}, status=status.HTTP_409_CONFLICT)
            serializer = CandidatesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        elif userType == 'E':
            try:
                name = request.data['name']
                type = request.data['type']
                billing_address = request.data['billing_address']
                website = request.data['website']
                number_of_employees = request.data['number_of_employees']
                data = {
                    "name": name,
                    "type": type,
                    "billing_address": billing_address,
                    "website": website,
                    "number_of_employees": number_of_employees
                }
                accObj = Account.objects.filter(name=name)

            except(BaseException, Exception) as e:
                var = "Error || Failure in RegisterView || \n \n" + traceback.format_exc()
                logger.error(var)                
                utils.send_error_email(var)
                return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            try:
                if len(accObj) == 0:
                    serializer = EmployerProfileSerializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    # return Response(serializer.data)
                    employerObj = Contact.objects.filter(email= request.data['email']).first()

                    if employerObj:
                        account = Account.objects.get(name=name)
                        account.delete()
                        return Response({"Error": "Email id already exists ,Kindly register again with different email"},status=status.HTTP_409_CONFLICT)



                    account = Account.objects.get(name=name)
                    S = EmployerProfileSerializer(account)
                    main_data = {
                        "account": S.data['employer_details_id'],
                        "first_name": request.data['first_name'],
                        "last_name": request.data['last_name'],
                        "mobile_phone": request.data['mobile_phone'],
                            "email": request.data['email'],
                            "password": request.data['password'],
                            "role": "Admin",
                        }   
                    serializer = EmployerAdminPostSerializer(data=main_data)
                    serializer.is_valid(raise_exception=True)
                    #serializer.save()
                else:
                        return Response({"Error": "Account Already Exists"}, status=status.HTTP_409_CONFLICT)

            except(BaseException, Exception) as e:
                account = Account.objects.filter(name=name)
                account.delete()
                var = "Error || Failure in RegisterView || \n \n" + traceback.format_exc()
                logger.error(var)                
                utils.send_error_email(var)
                return Response({"message": f"Authentication Failed, {e} "},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Error": "User type not supported"}, status=status.HTTP_406_NOT_ACCEPTABLE)

               
        payload = {
            'email': request.data['email'],
            'userType': userType,
            'iat': datetime.datetime.utcnow()
            }   
        token = jwt.encode(payload, config('JWT_SECRET'), algorithm='HS256')

        try:
            send_verify_email_mail(request.data['email'], token)
        except(BaseException, Exception) as e:
            var = "Error || Failure in RegisterView || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"message": f" verfification email sending failed, {e} "},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response = Response()
        response.data = {
            "message": "Registration Success. Verification Email Sent",
        }   
       
                               
        return response


class LoginView(APIView):
    def post(self, request):
        try:
            # logger.error("Error || Failure in LoginView || \n \n")
            userType = request.headers['userType']
            email = request.data['email']
            password = request.data['password']

            if userType == 'C':
                user = Candidate.objects.filter(email=email).first()

                if user is None:
                    return Response({"Error": "User not found,Kindly enter valid email address"}, status=status.HTTP_404_NOT_FOUND)

                if user.email_verification == False:
                    return Response({"Error": "User Not Verifed, Kindly Verify Email Before Login!"}, status=status.HTTP_403_FORBIDDEN)


                payload = {
                    'id': user.id,
                    'userType': userType,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=config('JWT_EXP', cast=int)),
                    'iat': datetime.datetime.utcnow()
                }
            elif userType == 'E':
                user = Contact.objects.filter(email=email).first()
              

                if user is None:
                    return Response({"Error": "User not found,Kindly enter valid email address"}, status=status.HTTP_404_NOT_FOUND)

                if user.account.bgv_completed == False:
                    return Response({"Error": "Account BGV still pending ,Kindly contact KYW team"}, status=status.HTTP_403_FORBIDDEN)

                if user.email_verified == False:
                     return Response({"Error": "User Not Verifed, Kindly Verify Email Before Login!"}, status=status.HTTP_403_FORBIDDEN)

                if user.status == "Inactive":
                    return Response({"Error": "User is inactive,Kindly contact your admin"}, status=status.HTTP_403_FORBIDDEN)

                payload = {
                    'id': user.account.id,
                    'member_id': user.id,
                    'userType': userType,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=config('JWT_EXP', cast=int)),
                    'iat': datetime.datetime.utcnow()
                }
            else:
                return Response({"Error": "User type not supported"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            # if user is None:
            #     raise NotFound({"Error':'User not found,Kindly enter valid email address'},code='404')

            if not check_password(password, user.password):
                return Response({"Error": "User Credentials are not valid"}, status=status.HTTP_403_FORBIDDEN)


            token = jwt.encode(payload, config('JWT_SECRET'), algorithm='HS256')
            response = Response()
            env = config('DEPLOY_ENV')

            if env == 'dev':
                response.set_cookie(key='jwt', value=token, httponly=True, secure=True, samesite='None')
            else:
                response.set_cookie(key='jwt', value=token, httponly=True)

            response.data = {
                "message": "Login Success"
            }
            return response

        except(BaseException, Exception) as e:
            var = "Error || Failure in LoginView || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserView(APIView):
    def get(self, request):
        
        response = Response()
        payload,response = utils.validate_token(self, request, response)

        try:

            if payload['userType'] == 'C':
                user = Candidate.objects.using('salesforce').filter(id=payload['id']).first()
                serializer = CandidateSerializer(user)
            elif payload['userType'] == 'E':
                user = Contact.objects.using('salesforce').filter(id=payload['member_id']).first()
                serializer = EmployerAdminSerializer(user)

            response.data = serializer.data
            return response

        except(BaseException, Exception) as e:
            var = "Error || Failure in UserView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogOutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "Success"
        }
        return response


class VerifyEmailView(APIView):

    def get(self, request):

        try:
            userType = request.headers['userType']
            email = request.GET.get('email')

            if userType == 'C':
                user = Candidate.objects.filter(email=email).first()
            elif userType == 'E':
                user = Contact.objects.filter(email=email).first()
            else:
                return Response({"Error": "User type not supported"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            if user is None:
                return Response({"Error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            payload = {
                'email': email,
                'userType': userType,
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, config('JWT_SECRET'), algorithm='HS256')

            send_verify_email_mail(email, token)
            return Response({"message": "Verification Email Sent Again. Please Verify"})

        except(BaseException, Exception) as e:
            var = "Error || Failure in VerifyEmailView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, token):
        # userType = request.headers['userType'] 
        try:
            payload = jwt.decode(token, config('JWT_SECRET'), algorithms=['HS256'], verify_exp=False)
        except jwt.ExpiredSignatureError:
            return Response({"Error":'Invalid Email Verification token.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            if payload['userType'] == 'C':
                user_obj = Candidate.objects.using('salesforce').filter(email=payload['email']).first()
            elif payload['userType'] == 'E':
                user_obj = Contact.objects.using('salesforce').filter(email=payload['email']).first()
                if user_obj.email_verified == True:
                    return Response({"message": "Email already Verified. Please Login"})
                else:
                    user_obj.email_verified = True
                    user_obj.save()
                    return Response({"message": "Email Verified. Please Login"})
            else:
                return Response({"Error": "User type not supported"},status=status.HTTP_406_NOT_ACCEPTABLE)
            if user_obj.screening_stages == 'Draft':
                user_obj.email_verification = True

                user_obj.screening_stages = 'Email Verified'
                user_obj.save()
                return Response({"message": "Email Verified. Please Login"})
            else:
                return Response({"message": "Email already Verified. Please Login"})

        except(BaseException, Exception) as e:
            var = "Error || Failure in VerifyEmailView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)       


class Forgotpassword(APIView):

    def post(self, request):
        try:
            candidate = Candidate.objects.filter(email=request.data['email']).first()
            employer = Contact.objects.filter(email=request.data['email']).first()
            if candidate:
                userType = 'C'
            
            elif employer:
                userType = 'E'
            
            else:
                return Response({"Error": "User not found,Kindly enter valid email address"}, status=status.HTTP_404_NOT_FOUND)

            payload = {
                'email': request.data['email'],
                'userType': userType,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=config('JWT_EXP', cast=int)),
                'iat': datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, config('JWT_SECRET'), algorithm='HS256')
            send_forget_password_mail(request.data['email'], token)
            return Response({"message": "Reset Password Email Sent."})

        except(BaseException, Exception) as e:
            var = "Error || Failure in Forgotpassword || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)       


class ChangePassword(APIView):
    def post(self, request, token):
        try:
            try:
                payload = jwt.decode(token, config('JWT_SECRET'), algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return Response({"Error": "Invalid  token for change password"},status=status.HTTP_401_UNAUTHORIZED)

            new_password = request.data['new_password']

            if payload['userType'] == 'C':
                user_obj = Candidate.objects.using('salesforce').filter(email=payload['email']).first()
            elif payload['userType'] == 'E':
                user_obj = Contact.objects.using('salesforce').filter(email=payload['email']).first()
            else:
                return Response({"Error": "User type not supported"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            password = make_password(new_password)
            user_obj.password = password
            user_obj.save()
            return Response({"message": "Password Changed Sucessfully -- Login Again"})

        except(BaseException, Exception) as e:
            var = "Error || Failure in ChangePassword || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        


def extendTokenExp(token, resp):
    remTime = token['exp'] - timegm(datetime.datetime.utcnow().utctimetuple())
    if remTime <= 30:
        token = {
            'id': token['id'],
            'userType': token['userType'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=config('JWT_EXP', cast=int)),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(token, config('JWT_SECRET'), algorithm='HS256')
        env = config('DEPLOY_ENV')
        if env == 'dev':
            resp.set_cookie(key='jwt', value=token, httponly=True, secure=True, samesite='None')
        else:
            resp.set_cookie(key='jwt', value=token, httponly=True)


def send_forget_password_mail(email, token):
    subject = 'KYW - Reset Password link'
    message = 'Hi,\nClick on the link to reset your password ' + config(
        'DOMAIN') + f'/api/auth/change-password/{token}/'
    email_from = configur['emailDetails']['emailfrom']
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


def send_verify_email_mail(email, token):
    subject = 'KYW - Welcome: Verify Your Email'
    message = 'Hi,\nYou are registered with Know Your Worth.\nPlease, click on the link to verify your email ' + config(
        'DOMAIN') + f'/api/auth/verify-mail/{token}/'
    email_from = configur['emailDetails']['emailfrom']
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


def send_registration_email(email, token):
    subject = 'KYW - Welcome: Verify Your Email'
    message = config('DOMAIN') + f'/api/auth/register/{token}/'
    email_from = configur['emailDetails']['emailfrom']
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True



class RegisterTeamView(APIView):

    def post(self, request, token):
        try:
            try:
                payload = jwt.decode(token, config('JWT_SECRET'), algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return Response({"Error": "Invalid  token for change password"}, status=status.HTTP_401_UNAUTHORIZED)

            contactObj=Contact.objects.filter(email=payload['email'])

            if contactObj:
                return Response({"Error":"Member with same email address already registered"},status=status.HTTP_403_FORBIDDEN)

            main_data = {
                "account": payload['id'],
                "first_name": request.data['first_name'],
                "last_name": request.data['last_name'],
                "mobile_phone": request.data['mobile_phone'],
                "email": payload['email'],
                "password": request.data['password'],
                "role": payload['role'],
                "email_verified": True
            }

           
            serializer = EmployerAdminPostSerializer(data=main_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({"message": "Registration Successful, Please login"})
        except(BaseException, Exception) as e:
            var = "Error || Failure in RegisterTeamView || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        


    
class ContactUs(APIView):

    def post(self, request):
        try:
            contact_us(request)
            #contact_us_acknowlegment(request)
            return Response({"message": "Thank you for Contacting KYW team  ,Someone from KYW will connect to you shortly"})

        except(BaseException, Exception) as e:
            var = "Error || Failure in ContactUs || \n \n" + traceback.format_exc()
            logger.error(var)            
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def contact_us(request):
    message = render_to_string("contact.html",{"from": request.data["from"], "name": request.data["name"], "msg": request.data["message"]})
    subject = "Email From Contact-us"
    email = EmailMessage(subject,message,configur['emailDetails']['emailfrom'], to =[ "surya@kyw.ai"])
    email.content_subtype = "html"
    email.send()

def contact_us_acknowlegment(request):
    message = render_to_string("acknowlegment.html",{ "name": request.data["name"]})
    subject = "KYW - Your Request Has been Recieved"
    email = EmailMessage(subject,message,configur['emailDetails']['emailfrom'], to =[request.data["from"]])
    email.content_subtype = "html"
    email.send()

    
def send_employee_status_email(email, status, admin_name, employee_name):
    subject = f'Profile Turned {status}'
    message = f'Admin : {admin_name}  has change profile status of {employee_name} to {status} stage'
    email_from = configur['emailDetails']['emailfrom']
    recipient_list = email
    send_mail(subject, message, email_from, recipient_list)
    return True
