from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import *
from .models import *
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
# from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib import auth
import random
from .backend import *


from django.shortcuts import render
from django.conf import settings
#from django.http.response import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.db.models import Q
from rest_framework import viewsets, status
import jwt
from django.conf import settings
import random
from django.http import JsonResponse


#to create signup API
class SignupAPIView(APIView):
    @csrf_exempt
    def post(self,request):
        data = request.data

        user_name=data.get('user_name')
        mail=data.get('mail')
        password=data.get('password')

        if CustomUser.objects.filter(Q(user_name=user_name)).exists():
            return Response({'Error':'User Already Exists'})
        else:
            data=CustomUser.objects.create(user_name=user_name,mail=mail,password=password)
            auth_token=jwt.encode(
                                    {
                                        'user_name':user_name,
                                        'mail':mail,
                                        'password':password
                                    },
                                    str(settings.JWT_SECRET_KEY), algorithm="HS256")
                                    #print(auth_token,'this is auth_token')

            authorization = 'Bearer'+' '+str(auth_token)
            print(auth_token,'this is auth_token')
            response_result = {}
            response = {}
            response_result['result'] = {
                            'result': {'Data': 'User Successfully Registered',
                            'token':authorization,
                            'user_id':data.id,
                            "user_name":user_name,

                            }}
            response['Authorization'] = authorization
            response['status'] = status.HTTP_200_OK
            return Response(response_result['result'], headers=response,status= status.HTTP_200_OK)


#to create login API
class LoginAPIView(APIView):
    #breakpoint()
    def post(self,request):
        data = request.data
        user_name =data.get("user_name")
        password=data.get("password")

        response = {}
        if CustomUser.objects.filter(Q(user_name=user_name)).exists():
            user =CustomUser.objects.get(Q(user_name=user_name))
            #data_dict = {}
            if user:
                auth_token = jwt.encode(
                    {'user_id':user.id,'user_name':user_name,'password':password,},
                    str(settings.JWT_SECRET_KEY), algorithm="HS256")
                authorization = 'Bearer'+' '+str(auth_token)
                response_result = {}
                response = {}
                response_result['result'] = {
                    'detail': 'Login successfull',
                    'user_id':user.id,
                    'token':authorization,
                    'status': status.HTTP_200_OK
                    }
                response['Authorization'] = authorization
                response['status'] = status.HTTP_200_OK
                return Response(response_result['result'], headers=response,status= status.HTTP_200_OK)
            else:
                header_response = {}
                response['error'] = {'error': {
                    'detail': 'Invalid Username / Password', 'status': status.HTTP_401_UNAUTHORIZED}}
                return Response(response['error'], headers=header_response,status= status.HTTP_401_UNAUTHORIZED)
        else:

            response['error'] = {'error': {
                    'detail': 'Invalid Username / Password', 'status': status.HTTP_401_UNAUTHORIZED}}
            return Response(response['error'], status= status.HTTP_401_UNAUTHORIZED)





from django.contrib.auth import authenticate
from django.core.mail import message, send_mail, EmailMessage
import inspect

otpsss= random.randint(100000, 999999)
forgotpass_otps=otpsss

#to create API for sending mail for OTP
class ForgotPassword_send_otp(APIView):

    def post(self, request):
        data = request.data

        mail = data.get('mail')

        user_check=CustomUser.objects.filter(mail=mail)
        for i in user_check:
            mail=i.mail
        if user_check:
            message = inspect.cleandoc('''Hello,\n%s is your OTP to Forgot Password to your jobportal.\nWith Warm Regards,\njobportal,
                                   ''' % (otpsss))
            send_mail(
                'Greetings from JOB PORTAL', message
                ,
                '@gmail.com',
                [mail],

            )
            data_dict = {}
            data_dict["Otp"] = otpsss
            da="OTP SENT"
            return Response(da)

        else:
            response="Invalid username"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


#to create API for verifing the OTP
class OTP_Verification_forgotpassAPIView(APIView):


    def post(self, request):
        data = request.data
        otp = data.get('otp')
        print(forgotpass_otps,'ori')
        print(otp,'ori')
        if otp:
            if int(otp)==int(forgotpass_otps):
                response="OTP matcheds successfully"
                return Response(response, status=status.HTTP_200_OK)
            else:
                response="Invalid otp"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response="otp required"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



# creat API to update the password
class ForgotPasswordUpdate(APIView):

    def post(self, request):
        data = request.data
        user_name = data.get('user_name')
        password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        user_check = CustomUser.objects.filter(user_name= user_name)

        if password == confirm_password:
            if user_check:
                user_data = CustomUser.objects.get(user_name= user_name)
                # user_data.set_password(password)
                user_data.save()

                message= 'Hello!\nYour password has been updated sucessfully. '
                subject= 'Password Updated Sucessfully '

                email = EmailMessage(subject, message, to=[user_data.mail])
                email.send()
                response="Password Updated Sucessfully"
                return Response(response, status=status.HTTP_200_OK)

            else:
                response="Please Enter Valid username"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response="Password did not matched"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)





            return Response(response, status=status.HTTP_400_BAD_REQUEST)



#to creating job portal APIs

class JobProfileAPIView(APIView):

#to get all the job profile
    def get(self, request):

        id =self.request.query_params.get('id')
        if id:
            profile = JobProfile.objects.filter(id=id).values()
            return Response(profile)
        else:

            profile = JobProfile.objects.all().values()
            return Response(profile)

#to post job portal profile
    def post(self, request):
        data = request.data

        job_profile_name = data.get('job_profile_name')
        discription= data.get('discription')

        jobcreate = JobProfile.objects.create(job_profile_name= job_profile_name, discription=discription )
        return Response("Data Added Sucessfully")


#to edit job portal profile
    def put(self, request):
        data = request.data
        id = data.get('id')
        if id:
            data = JobProfile.objects.filter(id=id).update(job_profile_name = data.get('job_profile_name'),discription=data.get('discription'))

            if data:
                    return JsonResponse({'message': 'data Updated Sucessfully.'})
            else:
                response={'message':"Invalid id"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)



        else:
            return JsonResponse({'message': 'Id Required.'})

#to delete job portal profile
    def delete(self, request):


        id =self.request.query_params.get('id')
        item = JobProfile.objects.filter(id= id)

        if len(item) > 0:
            item.delete()
            return Response("Item Deleted Sucessfully")
        else:
            return Response("Id Required.")



#create APIs for form
class CandidateFormAPIView(APIView):

#to get all the forms
    def get(self, request):

        id =self.request.query_params.get('id')
        if id:
            formdata = CandidateForm.objects.filter(id=id).values()
            return Response(formdata)
        else:

            formdata = CandidateForm.objects.all().values()
            return Response(formdata)


#to post the forms
    def post(self, request):
        data = request.data
        jobProfile_id=data.get('jobProfile_id')
        candidate_name = data.get('candidate_name')
        candidate_old_company= data.get('candidate_old_company')
        previous_CTC=data.get('previous_CTC')
        expected_CTC=data.get('expected_CTC')
        location=data.get('location')
        pdf_CV=request.FILES['pdf_CV']


        formcreate = CandidateForm.objects.create(candidate_name= candidate_name, candidate_old_company= candidate_old_company, previous_CTC=previous_CTC,expected_CTC=expected_CTC, location=location,
        jobProfile_id=jobProfile_id,pdf_CV=pdf_CV )
        return Response("Data Added Sucessfully")


#to edit the forms
    def put(self, request):
        data = request.data
        id = data.get('id')
        if id:
            data = CandidateForm.objects.filter(id=id).update(candidate_name = data.get('candidate_name'),
            jobProfile_id=data.get('jobProfile_id'),                  candidate_old_company= data.get('candidate_old_company'), previous_CTC=data.get('previous_CTC'), expected_CTC=data.get('expected_CTC'),
            pdf_CV=request.FILES['pdf_CV'], location=data.get('location'))

            if data:
                    return JsonResponse({'message': 'data Updated Sucessfully.'})
            else:
                response={'message':"Invalid id"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)


        else:
            return JsonResponse({'message': 'Id Required.'})


#to delete the form
    def delete(self, request):


        id =self.request.query_params.get('id')
        item = CandidateForm.objects.filter(id= id)

        if len(item) > 0:
            item.delete()
            return Response("Item Deleted Sucessfully")
        else:
            return Response("Id Required.")
