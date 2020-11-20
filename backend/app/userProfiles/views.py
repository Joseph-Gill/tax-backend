from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, UpdateAPIView


class RetrieveUpdateLoggedInUserProfile(RetrieveUpdateAPIView):
    """
    get:
    Retrieve the logged in User's Profile

    update:
    Update the logged in User's Profile
    """

    pass


class RetrieveLoggedInUserTasks(ListAPIView):
    """
    List the logged in User's Tasks
    """

    pass


class UpdateSpecificUserGroupOrProjectRole(UpdateAPIView):
    """
    Update a specified User's Group or Project Role
    """

    pass
