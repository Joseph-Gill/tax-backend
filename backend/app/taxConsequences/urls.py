from django.urls import path

from app.taxConsequences.views import ListAllOrCreateTaxConsequenceForSpecificStep, RetrieveUpdateDestroySpecificTaxConsequence, SetTaxConsequenceReviewedByLoggedInUser, SetTaxConsequenceNotReviewed, ListAllTaxConsequencesNotReviewedSameCountryAsUser

urlpatterns = [
    path('step/<int:step_id>/', ListAllOrCreateTaxConsequenceForSpecificStep.as_view(), name='list-create-tax-consequence'),
    path('tax/<int:tax_id>/', RetrieveUpdateDestroySpecificTaxConsequence.as_view(), name='retrieve-update-destroy-tax-consequence'),
    path('tax/<int:tax_id>/reviewed/', SetTaxConsequenceReviewedByLoggedInUser.as_view(), name='set-tax-reviewed-user'),
    path('tax/<int:tax_id>/notreviewed/', SetTaxConsequenceNotReviewed.as_view(), name='set-tax-not-reviewed'),
    path('project/<int:project_id>/notreviewed/samecountry/', ListAllTaxConsequencesNotReviewedSameCountryAsUser.as_view(), name='list-tax-consequence-not-reviewed-same-country-user')
]