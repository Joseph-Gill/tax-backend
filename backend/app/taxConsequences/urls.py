from django.urls import path

from app.taxConsequences.views import ListAllOrCreateTaxConsequenceForSpecificStep, RetrieveUpdateDestroySpecificTaxConsequence, SetTaxConsequenceReviewedByLoggedInUser

urlpatterns = [
    path('step/<int:step_id>/', ListAllOrCreateTaxConsequenceForSpecificStep.as_view(), name='list-create-tax-consequence'),
    path('tax/<int:tax_id>/', RetrieveUpdateDestroySpecificTaxConsequence.as_view(), name='retrieve-update-destroy-tax-consequence'),
    path('tax/<int:tax_id>/reviewed/', SetTaxConsequenceReviewedByLoggedInUser.as_view(), name='set-tax-reviewed-user')
]