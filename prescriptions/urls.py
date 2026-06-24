from django.urls import path

from .views import (
    dashboard,
    safety_report,
    download_report,
    search_drugs,
    drug_demo,
    new_prescription,
    edit_prescription,
    replace_drug,
)

urlpatterns = [

    path(
        '',
        dashboard,
        name='dashboard'
    ),

    path(
        'new-prescription/',
        new_prescription,
        name='new_prescription'
    ),

    path(
        'edit-prescription/<int:prescription_id>/',
        edit_prescription,
        name='edit_prescription'
    ),

    path(
        'report/<int:prescription_id>/',
        safety_report,
        name='report'
    ),

    path(
        'report/<int:prescription_id>/pdf/',
        download_report,
        name='download_report'
    ),

    path(
        'search-drugs/',
        search_drugs,
        name='search_drugs'
    ),

    path(
        'drug-demo/',
        drug_demo,
        name='drug_demo'
    ),
    path(
    "replace-drug/<int:prescription_id>/",
    replace_drug,
    name="replace_drug"
)
]