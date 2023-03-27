from django.urls import path, include
from jobportalapp.views import *
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from . import views



app_name = 'jobportalapp'


router = routers.DefaultRouter()

#to add the url
urlpatterns = [
    path('', include(router.urls)),


    path('Signup/', SignupAPIView.as_view()),
    path('Login/', LoginAPIView.as_view(), name="LOGIN"),

    path('form/', CandidateFormAPIView.as_view(), name="FORM"),
    path('jobprofile/', JobProfileAPIView.as_view(), name="JOBPROFILE"),
    path('ForgotPassword_send_otp/',ForgotPassword_send_otp.as_view()),#
    path('OTP_Verification_forgotpass/',OTP_Verification_forgotpassAPIView.as_view()),#
    path('ForgotPasswordUpdate/', ForgotPasswordUpdate.as_view()),#




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
