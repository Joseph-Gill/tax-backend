from django.urls import path
from app.social_auth.views import SocialTokenConvertView

app_name = 'social_auth'

urlpatterns = [
    path('convert-token/', SocialTokenConvertView.as_view(), name='convert-token-and-user'),
]
