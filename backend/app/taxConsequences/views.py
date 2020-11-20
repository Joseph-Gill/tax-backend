from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ListAllOrCreateTaxConsequenceForSpecificStep(ListCreateAPIView):
    """
    get:
    List all Tax Consequences for a specified Step

    post:
    Create a new Tax Consequence for a specified Step
    """
    pass


class RetrieveUpdateDestroySpecificTaxConsequence(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a specified Tax Consequence

    update:
    Update a specified Tax Consequence

    delete:
    Delete a specified Tax Consequence
    """
    pass
