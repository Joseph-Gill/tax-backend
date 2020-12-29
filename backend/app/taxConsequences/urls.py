from django.urls import path

from app.taxConsequences.views import ListAllOrCreateTaxConsequenceForSpecificStep, RetrieveUpdateDestroySpecificTaxConsequence

urlpatterns = [
    path('step/<int:step_id>/', ListAllOrCreateTaxConsequenceForSpecificStep.as_view(), name='list-create-tax-consequence'),
    path('tax/<int:tax_id>/', RetrieveUpdateDestroySpecificTaxConsequence.as_view(), name='retrieve-update-destroy-tax-consequence')
]