from django.contrib import admin
from .models import (
    Drug,
    DrugInteraction,
    DrugAlternative
)

admin.site.register(Drug)
admin.site.register(DrugInteraction)
admin.site.register(DrugAlternative)