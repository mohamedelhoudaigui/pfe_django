# core/admin.py
from django.contrib import admin
from .models import CivilServant, JobDetail, SalaryDetail, Categorie, Grade, EchelonIndice

admin.site.register(CivilServant)
admin.site.register(JobDetail)
admin.site.register(SalaryDetail)
admin.site.register(Categorie)
admin.site.register(Grade)
admin.site.register(EchelonIndice)