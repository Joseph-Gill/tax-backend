from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from app.groups.models import Group
from app.organizations.models import Organization
from app.organizations.serialziers import OrganizationSerializer


class ListAllOrCreateOrganizationForGroup(ListCreateAPIView):
    """
    get:
    List all Organizations

    post:
    Create a new Organization
    """
    queryset = Group
    serializer_class = OrganizationSerializer
    lookup_url_kwarg = 'group_id'
    permission_classes = []

    def list(self, request, *args, **kwargs):
        target_group = self.get_object()
        organizations = target_group.organizations.all().order_by('name')
        serializer = self.get_serializer(organizations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        target_group = self.get_object()
        new_organization = Organization(
            name=request.data['name']
        )
        new_organization.save()
        target_group.organizations.add(new_organization)
        target_group.save()
        serializer = self.get_serializer(new_organization)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
    lookup_url_kwarg = 'org_id'
