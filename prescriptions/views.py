from django.shortcuts import render
from patients.models import Patient
from .models import Prescription
from .checker import (
    check_interactions,
    check_allergies,
    check_contraindications,
    get_drug_information,
)
from .models import PrescriptionDrug
from .models import Prescription
from django.http import HttpResponse
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet
from interactions.models import Drug
from django.http import JsonResponse
from django.shortcuts import redirect
from patients.models import Patient
from patients.models import Patient
from prescriptions.models import Prescription
from datetime import date, timedelta
from interactions.models import DrugAlternative
def dashboard(request):

    patients = Patient.objects.all().order_by("-id")[:5]

    prescriptions = Prescription.objects.all().order_by("-id")[:5]
    upcoming_followups = Prescription.objects.filter(
    follow_up_date__isnull=False    
    ).order_by("follow_up_date")[:5]
    context = {
    "patients": patients,
    "prescriptions": prescriptions,
    "patient_count": Patient.objects.count(),
    "prescription_count": Prescription.objects.count(),
    "today": date.today(),
    "upcoming_followups": upcoming_followups,
}

    return render(
        request,
        "prescriptions/dashboard.html",
        context
    )
def safety_report(request, prescription_id):
    from .checker import get_alternatives
    prescription = Prescription.objects.get(
        id=prescription_id
    )

    drugs = PrescriptionDrug.objects.filter(
        prescription=prescription
    )

    interactions = check_interactions(
    prescription
    )

    allergies = check_allergies(
        prescription
    )

    contraindications = check_contraindications(
        prescription
    )
    drug_info = get_drug_information(
    prescription
)
    alternatives = []

    if (
        interactions
        or allergies
        or contraindications
    ):

        alternatives = get_alternatives(
            prescription,
            allergies,
            contraindications
        )

    context = {
    "prescription": prescription,
    "drugs": drugs,
    "interactions": interactions,
    "allergies": allergies,
    "contraindications": contraindications,
    "drug_info": drug_info,
    "alternatives": alternatives,
}

    return render(
        request,
        "prescriptions/report.html",
        context,
    )
def download_report(request, prescription_id):

    prescription = Prescription.objects.get(
        id=prescription_id
    )

    drugs = PrescriptionDrug.objects.filter(
        prescription=prescription
    )

    interactions = check_interactions(
        prescription
    )

    allergies = check_allergies(
        prescription
    )

    contraindications = check_contraindications(
        prescription
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = (
        f'attachment; '
        f'filename="Prescription_{prescription_id}.pdf"'
    )

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "Prescription Safety Report",
            styles['Title']
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"Patient: {prescription.patient.name}",
            styles['Normal']
        )
    )

    story.append(
        Paragraph(
            f"Doctor: {prescription.doctor_name}",
            styles['Normal']
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "Medicines:",
            styles['Heading2']
        )
    )

    for drug in drugs:

        story.append(
            Paragraph(
                f"• {drug.drug_name} "
                f"({drug.dosage})",
                styles['Normal']
            )
        )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "Drug Interactions",
            styles['Heading2']
        )
    )

    if interactions:

        for alert in interactions:

            story.append(
                Paragraph(
                    f"{alert['drug1']} + "
                    f"{alert['drug2']} "
                    f"({alert['severity']})",
                    styles['Normal']
                )
            )

    else:

        story.append(
            Paragraph(
                "No interactions detected.",
                styles['Normal']
            )
        )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "Allergy Alerts",
            styles['Heading2']
        )
    )

    if allergies:

        for alert in allergies:

            story.append(
                Paragraph(
                    alert['message'],
                    styles['Normal']
                )
            )

    else:

        story.append(
            Paragraph(
                "No allergy alerts.",
                styles['Normal']
            )
        )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "Contraindications",
            styles['Heading2']
        )
    )

    if contraindications:

        for alert in contraindications:

            story.append(
                Paragraph(
                    alert['message'],
                    styles['Normal']
                )
            )

    else:

        story.append(
            Paragraph(
                "No contraindications detected.",
                styles['Normal']
            )
        )

    story.append(Spacer(1, 30))

    story.append(
        Paragraph(
            "Doctor Signature: __________",
            styles['Normal']
        )
    )

    doc.build(story)

    return response
def search_drugs(request):
    query = request.GET.get('term', '')

    drugs = Drug.objects.filter(
        name__icontains=query
    )[:10]

    results = [
        drug.name
        for drug in drugs
    ]

    return JsonResponse(
        results,
        safe=False
    )
def drug_demo(request):
    return render(
        request,
        'prescriptions/drug_demo.html'
    )
def new_prescription(request):

    patients = Patient.objects.all()

    if request.method == "POST":

        patient_id = request.POST.get("patient")

        doctor_name = request.POST.get("doctor")

        follow_up_date = request.POST.get(
            "follow_up_date"
        )

        patient = Patient.objects.get(
            id=patient_id
        )

        prescription = Prescription.objects.create(
            patient=patient,
            doctor_name=doctor_name,
            follow_up_date=follow_up_date
        )

        drug_names = request.POST.getlist(
            "drug_name"
        )

        dosages = request.POST.getlist(
            "dosage"
        )

        durations = request.POST.getlist(
            "duration"
        )

        for drug, dosage, duration in zip(
            drug_names,
            dosages,
            durations
        ):

            if drug.strip():

                PrescriptionDrug.objects.create(
                    prescription=prescription,
                    drug_name=drug,
                    dosage=dosage,
                    duration=duration
                )

        return redirect(
            "report",
            prescription_id=prescription.id
        )
    selected_patient = request.GET.get(
    "patient"
)
    return render(
    request,
    "prescriptions/new_prescription.html",
    {
        "patients": patients,
        "selected_patient": selected_patient,
    }
) 
def edit_prescription(
    request,
    prescription_id
):

    prescription = Prescription.objects.get(
        id=prescription_id
    )

    drugs = PrescriptionDrug.objects.filter(
        prescription=prescription
    )

    patients = Patient.objects.all()

    if request.method == "POST":

        patient_id = request.POST.get(
            "patient"
        )

        prescription.patient = Patient.objects.get(
            id=patient_id
        )

        prescription.doctor_name = request.POST.get(
            "doctor"
        )

        prescription.follow_up_date = request.POST.get(
            "follow_up_date"
        )

        prescription.save()

        drug_names = request.POST.getlist(
            "drug_name"
        )

        dosages = request.POST.getlist(
            "dosage"
        )

        durations = request.POST.getlist(
            "duration"
        )

        existing_drugs = list(drugs)

        for i, drug in enumerate(existing_drugs):

            if i < len(drug_names):

                drug.drug_name = drug_names[i]

                drug.dosage = dosages[i]

                drug.duration = durations[i]

                drug.save()

        return redirect(
            "report",
            prescription_id=prescription.id
        )

    return render(
        request,
        "prescriptions/edit_prescription.html",
        {
            "prescription": prescription,
            "drugs": drugs,
            "patients": patients,
        }
    )
def replace_drug(request, prescription_id):

    old_drug = request.GET.get(
        "old_drug"
    )

    new_drug = request.GET.get(
        "new_drug"
    )

    prescription = Prescription.objects.get(
        id=prescription_id
    )

    drug = PrescriptionDrug.objects.filter(
        prescription=prescription,
        drug_name=old_drug
    ).first()

    if drug:

        drug.drug_name = new_drug

        drug.save()

    return redirect(
        "report",
        prescription_id=prescription.id
    )