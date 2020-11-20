from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ListAllOrCreateOrganization(ListCreateAPIView):
    """
    get:
    List all Organizations

    post:
    Create a new Organization
    """
    pass


class RetrieveUpdateDestroySpecificOrganization(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a specified Organization

    update:
    Update a specified Organization

    delete:
    Delete a specified Organization
    """
    pass
