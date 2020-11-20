from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ListAllOrCreateProjectForSpecificGroup(ListCreateAPIView):
    """
    get:
    List all Projects for a specified Group

    post:
    Create a new Project for a specified Group
    """
    pass


class RetrieveUpdateDestroySpecificProject(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a specified Project

    update:
    Update a specified Project

    delete:
    Delete a specified Project
    """
    pass
