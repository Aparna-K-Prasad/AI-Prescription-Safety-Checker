from datetime import date
from django.db import models


class Patient(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)

    date_of_birth = models.DateField()

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES
    )

    allergies = models.TextField(
        blank=True
    )

    diseases = models.TextField(
        blank=True
    )

    @property
    def age(self):

        today = date.today()

        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                <
                (
                    self.date_of_birth.month,
                    self.date_of_birth.day
                )
            )
        )

    def __str__(self):
        return self.name