from rest_framework import status, exceptions, serializers
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from app.users.serializers import UserSerializer

from django.contrib.auth import authenticate

User = get_user_model()


class SocialTokenConvertSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super(serializers.Serializer, self).__init__(*args, **kwargs)
        self.fields['convert_token'] = serializers.CharField()

    def validate(self, attrs):
        authenticate_kwargs = {
            'convert_token': attrs['convert_token'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        # Prior to Django 1.10, inactive users could be authenticated with the
        # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
        # prevents inactive users from authenticating.  App designers can still
        # allow inactive users to authenticate by opting for the new
        # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
        # users from authenticating to enforce a reasonable policy and provide
        # sensible backwards compatibility with older Django versions.
        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        data = {}

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class SocialTokenConvertView(TokenObtainPairView):
    serializer_class = SocialTokenConvertSerializer

    """
    post:
    Create a new session for a user. Sends back tokens and user.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        user_serializer = UserSerializer(instance=serializer.user)
        res = {
            'user': user_serializer.data,
            **serializer.validated_data
        }

        return Response(res, status=status.HTTP_200_OK)
