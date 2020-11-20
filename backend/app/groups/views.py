from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ListAllOrCreateGroup(ListCreateAPIView):
    """
    get:
    List all Groups

    post:
    Create a new Group
    """
    pass


class RetrieveUpdateDestroySpecificGroup(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a specified Group

    update:
    Update a specified Group

    delete:
    Delete a specified Group
    """
    pass
