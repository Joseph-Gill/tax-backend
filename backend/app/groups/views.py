from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework import status
from app.emails.signals import send_email
from app.entities.models import Entity
from app.groups.models import Group
from app.groups.serializers import GroupSerializer
from rest_framework.response import Response
from app.groups.signals import post_user_group_creation
from app.registration.serializers import RegistrationSerializer
from app.userProfiles.models import UserProfile
from django.contrib.auth import get_user_model
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
        name = serializer.data['name']
        new_group = Group(
            name=name
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


class AddRemoveUserInSpecificGroup(CreateAPIView):
    """
    Toggle a specified User being a member of a specified Group
    """
    serializer_class = RegistrationSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        target_user = User.objects.filter(email=request.data["email"])
        target_group = Group.objects.filter(id=kwargs['group_id'])[0]
        if target_user:
            target_user_profile = target_user[0].user_profile
            if target_group in target_user_profile.groups.all():
                target_user_profile.groups.remove(target_group)
            else:
                target_user_profile.groups.add(target_group)
                if target_group == target_user[0].registration_profile.inviting_group:
                    target_user[0].registration_profile.inviting_group = None
                    target_user[0].registration_profile.save()
                # Need to add sending them an email to the User informing them they were added to a Group
                send_email.send(sender=Group, request=request, to=target_user[0].email, email_type='added_to_group')
            return Response(status=status.HTTP_201_CREATED)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            target_user = serializer.save(serializer.validated_data)
            target_user.registration_profile.inviting_group = target_group
            target_user.registration_profile.save()
            return Response(status=status.HTTP_202_ACCEPTED)


class DestroyUserFromNewUserList(DestroyAPIView):
    """
    Delete a new User from a specified Group's new User list
    """
    queryset = Group.objects.all()
    lookup_url_kwarg = 'group_id'

    def delete(self, request, *args, **kwargs):
        target_group = self.get_object()
        target_user = User.objects.filter(id=request['email'])
        if target_user.registration_profile.inviting_group == target_group:
            target_user.registration_profile.inviting_group = None
        return Response(status=status.HTTP_202_ACCEPTED)
