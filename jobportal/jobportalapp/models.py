from django.db import models

from django.contrib.auth.models import User


#to create table to database
class JobProfile(models.Model):
    job_profile_name=models.CharField(max_length=100, null=True, blank=True)
    discription=models.CharField(max_length=500, null=True, blank=True)


class CustomUser(models.Model):
    user = models.ForeignKey(User,null=True, on_delete= models.CASCADE)
    user_name= models.CharField(max_length=50, null=True, blank=True)
    mail= models.EmailField(max_length=50, null=True, blank=True)
    password=models.CharField(max_length=50, null=True, blank=True)
    #mobile_number= models.CharField(max_length=20, null=True, blank=True)
    created =   models.DateTimeField(auto_now_add=True,verbose_name="Created",blank=True,null=True)



class CandidateForm(models.Model):
    jobProfile = models.ForeignKey(JobProfile,null=True, on_delete= models.CASCADE)
    candidate_name=models.CharField(max_length=50, null=True, blank=True)
    candidate_old_company=models.CharField(max_length=50, null=True, blank=True)
    previous_CTC=models.CharField(max_length=50, null=True, blank=True)
    expected_CTC=models.CharField(max_length=50, null=True, blank=True)
    pdf_CV = models.FileField(upload_to= 'static/pdf', blank=True, null=True)

    location=models.CharField(max_length=50, null=True, blank=True)
    # Job Profile (dropdown)
    created =   models.DateTimeField(auto_now_add=True,verbose_name="Created",blank=True,null=True)
