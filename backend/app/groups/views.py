from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework import status
from app.emails.signals import send_email
from app.entities.models import Entity
from app.entityHistories.models import EntityHistory
from app.groups.models import Group
from app.groups.serializers import GroupSerializer, CreateGroupSerializer
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
    serializer_class = CreateGroupSerializer
    queryset = Group.objects.all()

    def perform_create(self, serializer):
        users_profile = UserProfile.objects.get(user=self.request.user)
        list_of_entities = json.loads(self.request.data['entities'])
        # create the new group in the database
        new_group = Group(
            name=serializer.validated_data.get('name'),
            avatar=serializer.validated_data.get('avatar')
        )
        new_group.save()
        # loop through list of entities to create
        for entity in list_of_entities:
            new_entity = Entity(
                name=entity['name'],
                location=entity['location'],
                legal_form=entity['legal_form'],
            )
            # give the entity an empty string for pid if it is the ultimate entity in the group
            if entity['pid'] == 'Ultimate':
                new_entity.pid = ''
            # find the parent entity and assign the pid to be the id of the parent entity
            else:
                target_parent = Entity.objects.get(group=new_group, name=entity['parent']['name'], location=entity['parent']['location'])
                new_entity.pid = target_parent.id
            # tax rate is optional
            if entity['tax_rate']:
                new_entity.tax_rate = float(entity['tax_rate'])
            new_entity.save()
            # add the entity to the new created group's entities
            new_group.entities.add(new_entity)
            # create a history entry for the creation of the entity by the group being created
            new_entity_history = EntityHistory(
                action='group_creation',
                entity=new_entity,
                creator=users_profile
            )
            new_entity_history.save()
        # add the group to the list of groups the logged in user is part of
        users_profile.groups.add(new_group)
        post_user_group_creation.send(sender=Group, user_profile=users_profile, name=serializer.validated_data.get('name'), new_group=new_group)


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
        users_profile = UserProfile.objects.get(user=self.request.user)
        target_group = self.get_object()
        # if there is a new avatar sent to update, it is updated
        if serializer.validated_data.get('avatar'):
            target_group.avatar = serializer.validated_data.get('avatar')
            target_group.save()
        # list of the groups entities before it was edited
        list_of_existing_entities = target_group.entities.all()
        # list of entities sent by the frontend after the group was edited
        list_of_new_entities = json.loads(self.request.data['entities'])
        for entity in list_of_new_entities:
            # if an entity has edited: true, a change was made to it during the edit process in the frontend
            if 'edited' in entity:
                # if an entity has a true pid, it is not the ultimate entity
                if entity['pid']:
                    # finds the target parent to use during the update process, name / location are unique pairings for a group
                    target_parent_entity = Entity.objects.get(group=target_group, name=entity['parent']['name'], location=entity['parent']['location'])
                # searches the list list_of_existing_entities for the entity
                result = next((x for x in list_of_existing_entities if x.id == entity['id']), None)
                # if it finds the entity, it updates it
                if result:
                    target_entity_to_update = Entity.objects.get(id=entity['id'])
                    target_entity_to_update.name = entity['name']
                    target_entity_to_update.location = entity['location']
                    target_entity_to_update.legal_form = entity['legal_form']
                    if entity['pid']:
                        target_entity_to_update.pid = target_parent_entity.id
                    if entity['tax_rate']:
                        target_entity_to_update.tax_rate = entity['tax_rate']
                    target_entity_to_update.save()
                    # create a history entry for the change of the entity
                    new_entity_history = EntityHistory(
                        action='group_edit_change',
                        entity=target_entity_to_update,
                        creator=users_profile
                    )
                    new_entity_history.save()
                # if it doesn't find it, it creates a new entity
                else:
                    new_entity = Entity(
                        pid=target_parent_entity.id,
                        name=entity['name'],
                        location=entity['location'],
                        legal_form=entity['legal_form'],
                    )
                    if entity['tax_rate']:
                        new_entity.tax_rate = float(entity['tax_rate'])
                    new_entity.save()
                    target_group.entities.add(new_entity)
                    # create a history entry for the creation of the entity by the group being edited
                    new_entity_history = EntityHistory(
                        action='group_edit_add',
                        entity=new_entity,
                        creator=users_profile
                    )
                    new_entity_history.save()
        # checks the list of list_of_existing_entities if it finds an entity that was not in the list_of_new_entities it permanently removes it
        for existing_entity in list_of_existing_entities:
            result = next((x for x in list_of_new_entities if x['id'] == existing_entity.id), None)
            if not result:
                existing_entity.delete()


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


class RetrieveAllAndFavoriteGroupsForUser(RetrieveAPIView):
    """
    List all the Groups, and all the favorite Groups of a the logged in User
    """

    serializer_class = GroupSerializer

    def retrieve(self, request, *args, **kwargs):
        target_user_profile = UserProfile.objects.get(user=request.user)
        user_groups = []
        for group in target_user_profile.groups.all():
            group_info = self.get_serializer(group).data
            group_info['user_favorite'] = target_user_profile in group.favorite_users.all()
            user_groups.append(group_info)
        return Response(user_groups, status=status.HTTP_200_OK)


class ToggleUserFavoriteGroupStatus(CreateAPIView):
    """
    Toggle favorite status for a specified Group for the logged in User
    """
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    lookup_url_kwarg = 'group_id'

    def post(self, request, *args, **kwargs):
        target_group = self.get_object()
        target_user_profile = UserProfile.objects.get(user=request.user)
        if target_user_profile in target_group.favorite_users.all():
            target_group.favorite_users.remove(target_user_profile)
            response_data = self.get_serializer(target_group)
            return Response(response_data.data, status=status.HTTP_200_OK)
        else:
            target_group.favorite_users.add(target_user_profile)
            response_data = self.get_serializer(target_group)
            return Response(response_data.data, status=status.HTTP_201_CREATED)
