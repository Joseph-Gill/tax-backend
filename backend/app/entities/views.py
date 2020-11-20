from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ListAllOrCreateEntity(ListCreateAPIView):
    """
    get:
    List all Entities

    post:
    Create a new Entity
    """
    pass


class RetrieveUpdateDestroySpecificEntity(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a specified Entity

    update:
    Update a specified Entity

    delete:
    Delete a specified Entity
    """
    pass
