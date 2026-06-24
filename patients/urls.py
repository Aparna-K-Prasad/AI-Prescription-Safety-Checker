from django.urls import path

from .views import (
    new_patient,
    patient_list,
    patient_detail,
    edit_patient,
)

urlpatterns = [

    path(
        "new-patient/",
        new_patient,
        name="new_patient"
    ),

    path(
        "patients/",
        patient_list,
        name="patient_list"
    ),

    path(
        "patient/<int:patient_id>/",
        patient_detail,
        name="patient_detail"
    ),

    path(
        "edit/<int:patient_id>/",
        edit_patient,
        name="edit_patient"
    ),

]