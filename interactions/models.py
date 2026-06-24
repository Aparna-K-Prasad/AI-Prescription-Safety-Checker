from django.db import models


class Drug(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    category = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return self.name


class DrugInteraction(models.Model):

    SEVERITY_CHOICES = [
        ('High', 'High'),
        ('Moderate', 'Moderate'),
        ('Low', 'Low'),
    ]

    drug1 = models.CharField(
        max_length=100
    )

    drug2 = models.CharField(
        max_length=100
    )

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES
    )

    risk = models.TextField()

    recommendation = models.TextField()

    def __str__(self):
        return (
            f"{self.drug1} + {self.drug2}"
        )


class DrugAlternative(models.Model):

    drug_name = models.CharField(max_length=100)

    alternative_name = models.CharField(max_length=100)

    reason = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return f"{self.drug_name} -> {self.alternative_name}"
class DrugInfo(models.Model):

    drug_name = models.CharField(
        max_length=100,
        unique=True
    )

    side_effects = models.TextField(
        blank=True
    )

    pregnancy_warning = models.TextField(
        blank=True
    )

    pediatric_warning = models.TextField(
        blank=True
    )

    max_daily_dosage = models.CharField(
        max_length=50,
        blank=True
    )

    def __str__(self):

        return self.drug_name