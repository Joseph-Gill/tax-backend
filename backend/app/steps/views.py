from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ListAllOrCreateStepForSpecificProject(ListCreateAPIView):
    """
    get:
    List all Steps for a specified Project

    post:
    Create a new Step for a specified Project
    """
    pass


class RetrieveUpdateDestroySpecificStep(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a specified Step

    update:
    Update a specified Step

    delete:
    Delete a specified Step
    """
    pass
