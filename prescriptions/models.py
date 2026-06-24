from django.db import models
from patients.models import Patient


class Prescription(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    doctor_name = models.CharField(
        max_length=100
    )

    follow_up_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"Prescription #{self.id} - "
            f"{self.patient.name}"
        )


class PrescriptionDrug(models.Model):

    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='drugs'
    )

    drug_name = models.CharField(
        max_length=100
    )

    dosage = models.CharField(
        max_length=50,
        blank=True
    )

    duration = models.CharField(
        max_length=50,
        blank=True
    )

    def __str__(self):
        return self.drug_name