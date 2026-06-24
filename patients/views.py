from django.shortcuts import render, redirect
from .models import Patient
from prescriptions.models import Prescription
from django.urls import reverse

def new_patient(request):

    if request.method == "POST":

        patient = Patient.objects.create(
            name=request.POST.get("name"),
            date_of_birth=request.POST.get(
                "date_of_birth"
            ),
            gender=request.POST.get("gender"),
            allergies=request.POST.get("allergies"),
            diseases=request.POST.get("diseases"),
        )

        return redirect(
            reverse("new_prescription")
            + f"?patient={patient.id}"
        )

    return render(
        request,
        "patients/new_patient.html"
    )
def patient_list(request):

    patients = Patient.objects.all()

    return render(
        request,
        "patients/patient_list.html",
        {
            "patients": patients
        }
    )
def patient_detail(request, patient_id):

    patient = Patient.objects.get(
        id=patient_id
    )

    prescriptions = Prescription.objects.filter(
        patient=patient
    ).order_by('-id')

    return render(
        request,
        "patients/patient_detail.html",
        {
            "patient": patient,
            "prescriptions": prescriptions
        }
    )
def edit_patient(request, patient_id):

    patient = Patient.objects.get(
        id=patient_id
    )

    if request.method == "POST":

        patient.name = request.POST.get("name")
        patient.gender = request.POST.get("gender")
        allergies = request.POST.get("allergies")
        diseases = request.POST.get("diseases")

        if allergies:
            patient.allergies = allergies

        if diseases:
            patient.diseases = diseases

        patient.save()

        return redirect(
            "patient_detail",
            patient_id=patient.id
        )

    return render(
        request,
        "patients/new_patient.html",
        {
            "patient": patient,
            "edit_mode": True
        }
    )