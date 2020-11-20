from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView


class ListAllChartsForSpecificProject(ListAPIView):
    """
    List all Charts for a specified Project
    """
    pass


class CreateChartForSpecificProjectStep(CreateAPIView):
    """
    Create a Chart for a specified Project Step
    """
    pass


class RetrieveUpdateDestroySpecificChart(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a specified Chart

    update:
    Update a specified Chart

    delete:
    Delete a specified Chart
    """
    pass
