from django.contrib import admin
from .models import Prescription, PrescriptionDrug


admin.site.register(Prescription)
admin.site.register(PrescriptionDrug)