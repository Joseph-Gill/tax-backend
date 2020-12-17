from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from app.groups.models import Group
from app.groups.serializers import GroupSerializer
from app.organizations.models import Organization
from app.organizations.serialziers import OrganizationSerializer


User = get_user_model()


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
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_organization = Organization(
            **serializer.validated_data
        )
        new_organization.save()
        target_group.organizations.add(new_organization)
        group_info = GroupSerializer(target_group)
        return Response(group_info.data, status=status.HTTP_201_CREATED)


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


class RetrieveOrganizationForSpecificUserGroup(RetrieveAPIView):
    """
    List the Organization shared by a specified User and specified Group
    """
    serializer_class = OrganizationSerializer
    queryset = Organization

    def retrieve(self, request, *args, **kwargs):
        target_user = User.objects.get(id=kwargs['user_id'])
        target_group = Group.objects.get(id=kwargs['group_id'])
        instance = Organization.objects.filter(user_profiles__user_id=target_user.id, group__id=target_group.id)
        if len(instance):
            serializer = self.get_serializer(instance[0])
            return Response(serializer.data)
        return Response({'organization': {'name': 'Not Assigned'}}, status=status.HTTP_204_NO_CONTENT)
