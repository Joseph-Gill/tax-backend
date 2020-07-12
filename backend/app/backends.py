from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from google.oauth2 import id_token
from google.auth.transport import requests

User = get_user_model()

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '325279088643-n4q940s55faovcj7ejtu9uafkccbkph6.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '3Le97UDz-CEeuheAfNsG_nYx'


class CustomGoogleBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjRlNGViZTQ4N2Q1Y2RmMmIwMjZhM2IyMjlkODZmMGQ0MjU4NDQ5ZmUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiMzI1Mjc5MDg4NjQzLW40cTk0MHM1NWZhb3ZjajdlanR1OXVhZmtjY2JrcGg2LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMzI1Mjc5MDg4NjQzLW40cTk0MHM1NWZhb3ZjajdlanR1OXVhZmtjY2JrcGg2LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTA0NTM5MDAxMjYzODAxMzczMDYzIiwiaGQiOiJwcm9wdWxzaW9uYWNhZGVteS5jb20iLCJlbWFpbCI6ImRhbmllbGVyQHByb3B1bHNpb25hY2FkZW15LmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiS2VOT0FuaWRBSUNWbUhmRDZUSmhEQSIsIm5hbWUiOiJEYW5pZWxlIFJvbmNhZ2xpb25pIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdncVBrOFc3REJMQ0lSRzkwWWMzNGNFc3o3bUdhNUg0YTVMdlVVPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IkRhbmllbGUiLCJmYW1pbHlfbmFtZSI6IlJvbmNhZ2xpb25pIiwibG9jYWxlIjoiZW4iLCJpYXQiOjE1OTQ1NTM3NzksImV4cCI6MTU5NDU1NzM3OSwianRpIjoiYjNjMzhkMTJmNjBlYzBlMjYyY2NhZGRjNDcwN2Q4MGE2NzZjMDg5ZCJ9.dsOIw1eH2R19X7gcwLt7IeqLE-uNgPT-okjmnKjC4DuJW66lQiRqfx28CD8KTyKe4ygz9XqHuWn88Fe3p3zGWOanulpPyvIMvlmEUiKtXAsaYM-V7nd3a4SamsuIIWPHJJdoGc1_aH6lqiFlzBdFIOD8nfEr3xYmXvAGcCv3lAgOYsZ_dGUQUn_3KhfCDe2KW-RYLb2Qa-AkPZrQOkLkfNFHJKNpru1L3LNqVo8qt1xwfI1pc8dIdrwuzJumuFderbSft3pNU3nLfLpd16143j0vPu8VdKrqX_zCBZMm_tcj2KzvEtS30Ci7pgDrJgUs0O1r6s7_s4R845imo6FRcA"
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), SOCIAL_AUTH_GOOGLE_OAUTH2_KEY)

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']

            if 'email_verified' not in idinfo:
                return None

            try:
                # Return user
                user = User.objects.get(email=idinfo.get('email'), is_active=True)
                return user
            except User.DoesNotExist:
                # Create user
                new_user = User(
                    email=idinfo.get('email'),
                    username=idinfo.get('email'),
                    is_active=True,
                    first_name=idinfo.get('given_name'),
                    last_name=idinfo.get('family_name'),
                )
                new_user.save()
                return new_user
        except ValueError:
            # Invalid token
            return None

    def get_user(self, user_id):
        try:
            user = User._default_manager.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None
