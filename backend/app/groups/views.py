from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework import status
from app.emails.signals import send_email
from app.entities.models import Entity
from app.groups.models import Group
from app.groups.serializers import GroupSerializer
from rest_framework.response import Response
from app.groups.signals import post_user_group_creation
from app.projects.models import Project
from app.registration.serializers import RegistrationSerializer
from app.userProfiles.models import UserProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
import json

User = get_user_model()


class ListAllOrCreateGroup(ListCreateAPIView):
    """
    get:
    List all Groups

    post:
    Create a new Group, and all its Entities
    """
    permission_classes = []
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    def perform_create(self, serializer):
        users_profile = UserProfile.objects.get(user=self.request.user)
        list_of_entities = json.loads(self.request.data['entities'])
        # name = serializer.data['name']
        new_group = Group(
            name=serializer.validated_data.get('name'),
            avatar=serializer.validated_data.get('avatar')
        )
        new_group.save()
        for entity in list_of_entities:
            if entity['pid'] == 'Ultimate':
                new_entity = Entity(
                    pid='',
                    name=entity['name'],
                    location=entity['location'],
                    legal_form=entity['legal_form'],
                    tax_rate=float(entity['tax_rate'])
                )
                new_entity.save()
                new_group.entities.add(new_entity)
            else:
                target_parent = Entity.objects.get(group=new_group, name=entity['pid'])
                new_entity = Entity(
                    pid=target_parent.id,
                    name=entity['name'],
                    location=entity['location'],
                    legal_form=entity['legal_form'],
                    tax_rate=float(entity['tax_rate'])
                )
                new_entity.save()
                new_group.entities.add(new_entity)
        users_profile.groups.add(new_group)
        post_user_group_creation.send(sender=Group, user_profile=users_profile, name=serializer.data['name'], new_group=new_group)


class ListAllUsersGroups(ListAPIView):
    """
    List all Groups of logged in User
    """
    serializer_class = GroupSerializer

    def list(self, request, *args, **kwargs):
        queryset = request.user.user_profile.groups.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveUpdateDestroySpecificGroup(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a specified Group

    update:
    Update a specified Group

    delete:
    Delete a specified Group
    """
    http_method_names = ['get', 'patch', 'delete']
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    lookup_url_kwarg = 'group_id'

    def perform_update(self, serializer):
        target_group = self.get_object()
        if serializer.validated_data.get('avatar'):
            target_group.avatar = serializer.validated_data.get('avatar')
            target_group.save()
        list_of_entities = json.loads(self.request.data['entities'])
        for entity in list_of_entities:
            target_parent=Entity.objects.get(group=target_group, name=entity['pid'])
            new_entity = Entity(
                pid=target_parent.id,
                name=entity['name'],
                location=entity['location'],
                legal_form=entity['legal_form'],
                tax_rate=float(entity['tax_rate'])
            )
            new_entity.save()
            target_group.entities.add(new_entity)


class AddUserInSpecificGroup(CreateAPIView):
    """
    Toggle a specified User being a member of a specified Group
    """
    serializer_class = RegistrationSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        target_user = User.objects.filter(email=request.data["email"])
        target_group = Group.objects.get(id=kwargs['group_id'])
        if target_user:
            # Need a way to check if the invited email has already been invited
            # by another group, but has not yet finalized their registration yet
            try:
                target_user_profile = UserProfile.objects.get(user=target_user[0])
                target_user_profile.groups.add(target_group)
                send_email.send(sender=Group, request=request, to=target_user[0].email, email_type='added_to_group')
                return Response(status=status.HTTP_201_CREATED)
            except UserProfile.DoesNotExist:
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            target_user = serializer.save(serializer.validated_data)
            target_user.registration_profile.inviting_group = target_group
            target_user.registration_profile.save()
            return Response(status=status.HTTP_201_CREATED)


class RemoveUsersFromGroupAndProjects(DestroyAPIView):
    """
    Delete an existing User from a specified Group and all the Group's Projects
    """
    queryset = Group.objects.all()
    lookup_url_kwarg = 'group_id'

    def destroy(self, request, *args, **kwargs):
        requesting_user = request.user
        match = check_password(request.data['password'], requesting_user.password)
        if match:
            target_group = self.get_object()
            list_of_users = self.request.data['users']
            for user in list_of_users:
                target_profile = UserProfile.objects.get(user__email=user['email'])
                target_group.users.remove(target_profile)
                target_project_roles = target_profile.assigned_project_roles.filter(project__group_id=target_group.id)
                if len(target_project_roles):
                    for role in target_project_roles:
                        self.perform_destroy(role)
            list_of_invited_users = self.request.data['invited_users']
            for user in list_of_invited_users:
                target_user = User.objects.get(email=user['email'])
                if target_user.registration_profile.inviting_group == target_group:
                    target_user.registration_profile.inviting_group = None
                    target_user.registration_profile.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RetrieveGroupForSpecificProject(RetrieveAPIView):
    """
    List the group a specified Project belongs to
    """

    queryset = Project.objects.all()
    lookup_url_kwarg = 'project_id'
    serializer_class = GroupSerializer

    def retrieve(self, request, *args, **kwargs):
        target_project = self.get_object()
        target_group = Group.objects.get(id=target_project.group.id)
        serializer = self.get_serializer(target_group)
        return Response(serializer.data)