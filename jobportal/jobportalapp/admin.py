from django.contrib import admin

from .models import *


#to show all the models table in admin panel
admin.site.register(CustomUser)
admin.site.register(CandidateForm)
admin.site.register(JobProfile)
