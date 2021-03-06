from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Feedback
from .serializers import FeedbackSerializer


class GetAllFeedback(ListAPIView):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()


class CreateFeedback(CreateAPIView):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
