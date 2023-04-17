from rest_framework.response import Response
import jwt , datetime
from decouple import config
from calendar import timegm
from rest_framework.exceptions import *
import configparser
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import rootpath
configur = configparser.ConfigParser()
configur.read(rootpath.get_project_root() + '/kyw_api_project/config.ini')

def extendTokenExp(token, resp):
    remTime = token['exp']-timegm(datetime.datetime.utcnow().utctimetuple())
    if remTime <= 600:
        token = {
            'id':token['id'],
            'userType' :token['userType'],
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=config('JWT_EXP', cast=int)),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(token, config('JWT_SECRET'), algorithm='HS256')
        env = config('DEPLOY_ENV')
        if  env == 'dev':
            resp.set_cookie(key='jwt', value=token, httponly=True, secure=True, samesite='None')
        else:
            resp.set_cookie(key='jwt', value=token, httponly=True) 


def validate_token(self,request,response):
    token = request.COOKIES.get('jwt')
    #response = Response()
    
    if not token:
        raise NotAuthenticated({"Error":'User Not Logged In!'})

    try:
        payload = jwt.decode(token, config('JWT_SECRET'), algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed({"Error":'Kindly Login Again!'})

    extendTokenExp(payload,response)

    return payload,response


def send_error_email(content):
    # recipients =['surya@kyw.ai','sreekar@kyw.ai']
    to = str(configur['error-email']['to']).split(',')
    cc = str(configur['error-email']['cc']).split(',')
    subject = 'KYW - Stage Error'
    message = content
    email_from = configur['emailDetails']['emailfrom']
    #send_mail(subject, message, email_from, recipient_list)
    email = EmailMessage(
            subject,
           message,
            email_from,
            to=to,
            cc=cc,
            reply_to=None
        )
    # email.content_subtype = "html"
    email.send(fail_silently=True)
    return True



    
