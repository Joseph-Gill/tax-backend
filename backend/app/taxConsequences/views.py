from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from app.projects.models import Project
from app.steps.models import Step
from app.taxConsequences.models import TaxConsequence
from app.taxConsequences.serializers import TaxConsequenceSerializer
from app.userProfiles.models import UserProfile


class ListAllOrCreateTaxConsequenceForSpecificStep(ListCreateAPIView):
    """
    get:
    List all Tax Consequences for a specified Step

    post:
    Create a new Tax Consequence for a specified Step
    """
    queryset = Step
    serializer_class = TaxConsequenceSerializer
    lookup_url_kwarg = 'step_id'

    def list(self, request, *args, **kwargs):
        target_step = self.get_object()
        tax_consequences = target_step.tax_consequences.all().order_by('location')
        serializer = self.get_serializer(tax_consequences, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        target_step = self.get_object()
        target_user_profile = UserProfile.objects.get(user=request.user)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_tax_consequence = TaxConsequence(
            **serializer.validated_data
        )
        new_tax_consequence.save()
        target_user_profile.created_tax_consequences.add(new_tax_consequence)
        target_step.tax_consequences.add(new_tax_consequence)
        return Response(status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroySpecificTaxConsequence(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a specified Tax Consequence

    update:
    Update a specified Tax Consequence, sets logged-in User as editing User

    delete:
    Delete a specified Tax Consequence
    """
    http_method_names = ['get', 'patch', 'delete']
    serializer_class = TaxConsequenceSerializer
    queryset = TaxConsequence.objects.all()
    lookup_url_kwarg = 'tax_id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        target_tax_consequence = self.get_object()
        serializer = self.get_serializer(target_tax_consequence, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        target_user_profile = UserProfile.objects.get(user=request.user)
        target_tax_consequence.editing_user = target_user_profile
        target_tax_consequence.save()
        return Response(serializer.data)


class SetTaxConsequenceReviewedByLoggedInUser(CreateAPIView):
    """
    Set a specified Tax Consequence as reviewed by the logged in User
    """

    queryset = TaxConsequence.objects.all()
    lookup_url_kwarg = 'tax_id'

    def create(self, request, *args, **kwargs):
        target_user_profile = UserProfile.objects.get(user=request.user)
        target_tax_consequence = self.get_object()
        target_tax_consequence.reviewed = True
        target_tax_consequence.save()
        target_user_profile.reviewed_tax_consequences.add(target_tax_consequence)
        return Response(status=status.HTTP_200_OK)


class SetTaxConsequenceNotReviewed(CreateAPIView):
    """
    Set a specified Tax Consequence as not reviewed
    """

    queryset = TaxConsequence.objects.all()
    lookup_url_kwarg = 'tax_id'

    def create(self, request, *args, **kwargs):
        target_tax_consequence = self.get_object()
        target_tax_consequence.reviewed = False
        target_tax_consequence.reviewing_user = None
        target_tax_consequence.save()
        return Response(status=status.HTTP_200_OK)


class ListAllTaxConsequencesNotReviewedSameCountryAsUser(ListAPIView):
    """
    List all Tax Consequences that are not reviewed and for the same country as the logged-in User
    """

    queryset = Project.objects.all()
    lookup_url_kwarg = 'project_id'
    serializer_class = TaxConsequenceSerializer

    def list(self, request, *args, **kwargs):
        target_project = self.get_object()
        target_user_profile = UserProfile.objects.get(user=request.user)
        target_tax_consequences = TaxConsequence.objects.filter(step__project=target_project, location=target_user_profile.country).exclude(reviewed=True)
        serializer = self.get_serializer(target_tax_consequences, many=True)
        return Response(serializer.data)


class GetOpenReviewTaxConsequenceNumbers(RetrieveAPIView):
    """
    Get the number of "Open" and "Not Reviewed" Tax Consequences of the logged-in User's country, for a specified Project
    """
    queryset = Project.objects.all()
    lookup_url_kwarg = 'project_id'

    def retrieve(self, request, *args, **kwargs):
        target_project = self.get_object()
        target_user_profile = UserProfile.objects.get(user=request.user)
        target_tax_consequences = TaxConsequence.objects.filter(location=target_user_profile.country, step__project=target_project).exclude(reviewed=True)
        comments_open = 0
        comments_to_review = 0
        for tax in target_tax_consequences:
            if not tax.description:
                comments_open = comments_open + 1
            else:
                comments_to_review = comments_to_review + 1
        tax_consequence_data = {
            'comments_open': comments_open,
            'comments_to_review': comments_to_review
        }
        return Response(tax_consequence_data, status=status.HTTP_200_OK)
