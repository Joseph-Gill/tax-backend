from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ListAllOrCreateTaskForSpecificStep(ListCreateAPIView):
    """
    get:
    List all Tasks for a specified Step

    post:
    Create a new Task for a specified Step
    """
    pass


class RetrieveUpdateDestroySpecificTask(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a specified Task

    update:
    Update a specified Task

    delete:
    Delete a specified Task
    """
    pass
