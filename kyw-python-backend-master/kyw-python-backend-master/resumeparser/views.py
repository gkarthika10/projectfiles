from django.shortcuts import render
from decouple import config
#DEBUG = config('DEBUG', cast=bool, default=True)

from rest_framework.views import    APIView
from rest_framework.response import Response
import json
import pandas as pd
import spacy
import csv
import numpy as np
from spacy import displacy
import re
from pdfminer.high_level import extract_text
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer,LTTextBox,LTTextBoxHorizontal
import requests
import io
import  pickle
from kyw_api_project import utils
import logging
import traceback
from rest_framework.exceptions import *
import boto3
logger = logging.getLogger('main')


def get_text(resume):
        text = extract_text(resume)
        return text

final_data={}

def get_fields(resume):
    
    dic ={}
    head=[]
    data=[]
    j=0
    for page_layout in extract_pages(resume):
    # 57.960,759.283,165.190,773.297C:\Users\j

        for element in page_layout:
            if isinstance(element,LTTextBoxHorizontal):
                al=[]
                for i in element.get_text().split("\n"):
                    if i!="":
                        if bool(re.match('[A-Z&/,\s]+$',i)):
                            head.append(i)
                    al.append(i)
                    data.append(i)
                dic[j]=al
                j+=1


    headinfo=[]
    for i in head:
        if i in data:
            headinfo.append(data.index(i))
    if(len(head)==0):
        return {}
    for i in range(len(head)):
        dic2={}
    for i in range(len(head)-1):
        dic2[head[i]]= data[headinfo[i]+1:headinfo[i+1]]

    
    for i in dic2.keys():


        list1= list(filter(None, dic2[i]))

        
        final_data[i.strip()]=list1
    
    
  


    return final_data


def get_resume_object(final_data):
    k=list(final_data.keys())
    resume_object={  }
    for i in k:
        if   i in ["ACADEMIC QUALIFICATIONS" , "EDUCATION"]:
            resume_object['EDUCATION']=(final_data[i])

        if  i in ['INTRODUCTION',"BASIC INFORMATION"] :
            resume_object['INTRODUCTION']=str(final_data[i])

        if   i in ["WORK EXPERIENCE" , "PROFESSIONAL EXPERIENCE" , "WORK HISTORY" , "EXPERIENCE"]:
            resume_object['WORK EXPERIENCE']=(final_data[i])
  


    return resume_object
# df_skills =pd.read_csv(r"resume\skills_extract.csv")

def extractSkills_model(text):
    s= set()
    dic={}
    nlp_skills=spacy.blank("en")

    # ruler = nlp_skills.add_pipe("entity_ruler")
    # patterns = [
    #     ]
    # ski=[]
    # ski=df_skills['skill_name'].tolist()
    # patterns = [
    #             {
    #                 "label": "GITHUB", "pattern": [{"TEXT": {"REGEX": "(?:https?:?\/\/)?(?:www\.)?github\.com\/(?P<login>[A-z0-9_-]+)\/?"}}]                                        
    #                 },
    #                 {
    #                     "label": "LINKEDIN", "pattern": [{"TEXT": {"REGEX":  r"(?:https?:?\/\/)?(?:[\w]+\.)?linkedin\.com\/in\/(?P<permalink>[\w\-\_À-ÿ%]+)\/?"}} ]
    #                 },
    #     {
    #     "label":"Email","pattern" : [{"LIKE_EMAIL": True}]   
    #     },
    #                 {
    #                     "label": "Mobile", "pattern": [{"TEXT": {"REGEX":  r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'}} ]
    #                 }
    #             ]

    # for i in ski:
    #     patterns.append( {"label": "SKILL", "pattern": i})
    # ruler.add_patterns(patterns)

    nlp = spacy.load('my_test_model')
    doc = nlp(text.lower().replace('•',""))
    for i in doc.ents:
        if i.label_ =="SKILL":
            if re.match('^[a-zA-Z\s]+$', i.text):
                s.add(i.text)
        else:
            dic[i.label_] = i.text

    dic['Skills'] = s


    return dic

class ParseResume(APIView):
 
      def post(self, request, *args, **kwargs):

        response=Response()
        payload,response=utils.validate_token(self,request,response)
        try:
            
            if payload["userType"]=='C':
                x=request.data['location']
                s3_client = boto3.client('s3')
                s3_bucket_name = 'kyw-resume-bucket'
                z = request.data['key']
                s3 = boto3.resource('s3',
                                    aws_access_key_id=config('ACCESS_KEY_ID'),
                                    aws_secret_access_key=config('SECRET_ACCESS_KEY'))

                obj = s3.Object(s3_bucket_name, z)
                fs = obj.get()['Body'].read()
                r1 = io.BytesIO(fs)
                #text = get_text(r1)

                text=get_text(r1)
                get_fields(r1)

                dic=get_resume_object(get_fields(r1))
                
                
                val=extractSkills_model(text = extract_text(r1))
            
                  
                dic['data']=val   

                return Response(dic)
            
            else:
                logger.error("Error || Not Valid User To get Profile Information || \n" )
                raise PermissionDenied({"Error": "This User is not authorized to perform this action."})

        except(BaseException, Exception) as e:
            var = "Error || Failure in LoginView || \n \n" + traceback.format_exc()
            logger.error(var)
            utils.send_error_email(var)
            return Response({"Error":"could not process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)