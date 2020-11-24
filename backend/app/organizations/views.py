from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from app.groups.models import Group
from app.organizations.models import Organization
from app.organizations.serialziers import OrganizationSerializer


class ListAllOrCreateOrganization(ListCreateAPIView):
    """
    get:
    List all Organizations

    post:
    Create a new Organization
    """
    serializer_class = OrganizationSerializer
    queryset = Group
    lookup_url_kwarg = 'group_id'
    permission_classes = []


class RetrieveUpdateDestroySpecificOrganization(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a specified Organization

    update:
    Update a specified Organization

    delete:
    Delete a specified Organization
    """
    http_method_names = ['get', 'patch', 'delete']
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    lookup_url_kwarg = 'group_id'
