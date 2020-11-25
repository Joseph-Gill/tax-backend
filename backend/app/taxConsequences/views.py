from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from app.steps.models import Step
from app.taxConsequences.models import TaxConsequence
from app.taxConsequences.serializers import TaxConsequenceSerializer


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
    permission_classes = []

    def list(self, request, *args, **kwargs):
        target_step = self.get_object()
        tax_consequences = target_step.tax_consequences.all().order_by('location')
        serializer = self.get_serializer(tax_consequences, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        target_step = self.get_object()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_tax_consequence = TaxConsequence(
            **serializer.validated_data
        )
        new_tax_consequence.save()
        target_step.tax_consequences.add(new_tax_consequence)
        return Response(status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroySpecificTaxConsequence(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a specified Tax Consequence

    update:
    Update a specified Tax Consequence

    delete:
    Delete a specified Tax Consequence
    """
    http_method_names = ['get', 'patch', 'delete']
    serializer_class = TaxConsequenceSerializer
    queryset = TaxConsequence.objects.all()
    lookup_url_kwarg = 'tax_id'
