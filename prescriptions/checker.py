from interactions.models import DrugInteraction
from .models import PrescriptionDrug
from interactions.models import DrugInfo
from interactions.models import DrugAlternative
ALLERGY_RULES = {
    "Penicillin": ["Amoxicillin"],
    "NSAIDs": ["Ibuprofen", "Aspirin", "Diclofenac"],
}
CONTRAINDICATION_RULES = {
    "Asthma": {
        "Propranolol":
        "Avoid in asthma patients."
    },

    "Kidney Disease": {
        "Ibuprofen":
        "Use cautiously in kidney disease."
    },

    "Pregnancy": {
        "Isotretinoin":
        "Contraindicated during pregnancy."
    }
}
def check_interactions(prescription):
    alerts = []

    drugs = list(
        PrescriptionDrug.objects.filter(
            prescription=prescription
        )
    )

    for i in range(len(drugs)):
        for j in range(i + 1, len(drugs)):

            drug1 = drugs[i].drug_name
            drug2 = drugs[j].drug_name

            interaction = DrugInteraction.objects.filter(
                drug1__iexact=drug1,
                drug2__iexact=drug2
            ).first()

            if not interaction:
                interaction = DrugInteraction.objects.filter(
                    drug1__iexact=drug2,
                    drug2__iexact=drug1
                ).first()

            if interaction:
                alerts.append({
                    "drug1": drug1,
                    "drug2": drug2,
                    "severity": interaction.severity,
                    "risk": interaction.risk,
                    "recommendation": interaction.recommendation,
                })

    return alerts
def check_allergies(prescription):
    alerts = []

    patient = prescription.patient

    patient_allergies = [
        allergy.strip()
        for allergy in patient.allergies.split(",")
        if allergy.strip()
    ]

    prescription_drugs = PrescriptionDrug.objects.filter(
        prescription=prescription
    )

    for allergy in patient_allergies:

        if allergy in ALLERGY_RULES:

            risky_drugs = ALLERGY_RULES[allergy]

            for drug in prescription_drugs:

                if drug.drug_name in risky_drugs:

                    alerts.append({
                        "allergy": allergy,
                        "drug": drug.drug_name,
                        "message":
                            f"Patient allergic to {allergy}. "
                            f"Avoid prescribing {drug.drug_name}."
                    })

    return alerts
def check_contraindications(prescription):
    alerts = []

    patient = prescription.patient

    diseases = [
        disease.strip()
        for disease in patient.diseases.split(",")
        if disease.strip()
    ]

    drugs = PrescriptionDrug.objects.filter(
        prescription=prescription
    )

    for disease in diseases:

        if disease in CONTRAINDICATION_RULES:

            risky_drugs = CONTRAINDICATION_RULES[disease]

            for drug in drugs:

                if drug.drug_name in risky_drugs:

                    alerts.append({
                        "disease": disease,
                        "drug": drug.drug_name,
                        "message":
                            risky_drugs[drug.drug_name]
                    })

    return alerts
def get_alternatives(
    prescription,
    allergies,
    contraindications
):

    suggestions = []

    risky_drugs = set()

    for alert in allergies:

        risky_drugs.add(
            alert["drug"]
        )

    for alert in contraindications:

        risky_drugs.add(
            alert["drug"]
        )

    for drug_name in risky_drugs:

        alternatives = DrugAlternative.objects.filter(
            drug_name__iexact=drug_name
        )

        for alt in alternatives:

            suggestions.append({

                "drug": drug_name,

                "alternative":
                    alt.alternative_name,

                "reason":
                    alt.reason,
            })

    return suggestions
def get_drug_information(prescription):

    warnings = []

    drugs = PrescriptionDrug.objects.filter(
        prescription=prescription
    )

    for drug in drugs:

        info = DrugInfo.objects.filter(
            drug_name__iexact=drug.drug_name
        ).first()

        if info:

            warnings.append({
                "drug": drug.drug_name,
                "side_effects": info.side_effects,
                "pregnancy": info.pregnancy_warning,
                "pediatric": info.pediatric_warning,
                "max_dose": info.max_daily_dosage,
            })

    return warnings