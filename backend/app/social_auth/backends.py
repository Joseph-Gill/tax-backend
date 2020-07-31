import json
import os
import urllib
import requests as py_request
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from google.oauth2 import id_token
from google.auth.transport import requests

from app.registration.signals import post_user_registration_validation, post_user_social_registration

User = get_user_model()


class GoogleOpenIdBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        if kwargs.get('backend') != 'googleOpenId':
            return None
        convert_token = kwargs.get('convert_token')
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(convert_token, requests.Request(), os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY'))

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

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
                post_user_registration_validation.send(sender=User, user=new_user)
                post_user_social_registration.send(sender=User, user=new_user)
                new_user.social_profile.social_avatar = idinfo.get('picture', '')
                new_user.social_profile.save()
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


class LinkedinOAuth2Backend(BaseBackend):
    def authenticate(self, request, **kwargs):
        if kwargs.get('backend') != 'linkedinOAuth2':
            return None
        convert_token = kwargs.get('convert_token')

        headers = {'Content-Type': 'x-www-form-urlencoded'}
        data = {
            'client_id': os.environ.get('SOCIAL_AUTH_LINKEDIN_OAUTH2_CLIENT_ID'),
            'client_secret': os.environ.get('SOCIAL_AUTH_LINKEDIN_OAUTH2_CLIENT_SECRET'),
            'grant_type': 'authorization_code',
            'code': convert_token,
            'redirect_uri': 'http://localhost:3000/login',
        }
        response_access_token = py_request.get('https://www.linkedin.com/oauth/v2/accessToken?' + urllib.parse.urlencode(data), headers=headers)
        access_token = json.loads(response_access_token.text).get('access_token')
        headers = {'Authorization': 'Bearer ' + access_token}

        response_user_email = py_request.get('https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))', headers=headers)
        email = json.loads(response_user_email.text).get('elements')[0].get('handle~').get('emailAddress')

        try:
            user = User.objects.get(email=email, is_active=True)
            return user
        except User.DoesNotExist:
            response_user_data = py_request.get('https://api.linkedin.com/v2/me/', headers=headers)
            user_data = json.loads(response_user_data.text)

            response_profile_pic = py_request.get('https://api.linkedin.com/v2/me?projection=(id,profilePicture(displayImage~:playableStreams),firstName,lastName)', headers=headers)
            profile_pic_url = json.loads(response_profile_pic.text).get('profilePicture').get('displayImage~').get('elements')[0].get('identifiers')[0].get('identifier')

            new_user = User(
                email=email,
                username=email,
                is_active=True,
                first_name=user_data.get('localizedLastName'),
                last_name=user_data.get('localizedFirstName'),
            )
            new_user.save()
            post_user_registration_validation.send(sender=User, user=new_user)
            post_user_social_registration.send(sender=User, user=new_user)
            new_user.social_profile.social_avatar = profile_pic_url
            new_user.social_profile.save()
            return new_user

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
