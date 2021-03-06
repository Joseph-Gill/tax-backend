from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers
from app.emails.signals import send_email
from app.groups.models import Group
from app.notifications.signals import notify_users
from app.registration.models import RegistrationProfile
from app.registration.models import code_generator
from app.registration.signals import post_user_password_reset_validation
from app.userProfiles.models import UserProfile

User = get_user_model()


def email_does_not_exist(email):
    try:
        User.objects.get(email=email)
        raise ValidationError(message='This email is taken')
    except User.DoesNotExist:
        return email


def email_does_exist(email):
    try:
        User.objects.get(email=email)
        return email
    except User.DoesNotExist:
        raise ValidationError(message='User does not exist!')


def username_does_not_exist(username):
    try:
        User.objects.get(username=username)
        raise ValidationError(message='This username is taken')
    except User.DoesNotExist:
        return username


def code_is_valid(code):
    try:
        reg_profile = RegistrationProfile.objects.get(code=code)
        if not reg_profile.code_used:
            return code
        else:
            raise ValidationError(message='This code has already been used!')
    except RegistrationProfile.DoesNotExist:
        raise ValidationError(message='This code is not valid!')


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(label='Registration E-Mail Address', validators=[email_does_not_exist])

    def save(self, validated_data):
        email = validated_data.get('email')
        new_user = User(
            email=email,
            is_active=False,
            username=email,
        )
        new_user.save()
        #####
        # Creating reg profile here and not with signal because signals are async
        # and I need the code in the reg profile right now.
        reg_profile = RegistrationProfile(
            user=new_user,
            code_type='RV'
        )
        reg_profile.save()
        #####
        send_email.send(sender=User, request=self.context['request'], to=email, email_type='registration_email', code=reg_profile.code)
        return new_user


class RegistrationValidationSerializer(serializers.Serializer):
    email = serializers.EmailField(label='Registration E-Mail Address', validators=[email_does_exist])
    code = serializers.CharField(label='Validation code', write_only=True, validators=[code_is_valid])
    password = serializers.CharField(label='password', write_only=True)
    password_repeat = serializers.CharField(label='password_repeat', write_only=True)
    first_name = serializers.CharField(label='First name', required=False)
    last_name = serializers.CharField(label='Last name', required=False)
    phone_number = serializers.CharField(label='phone number', required=False)
    country = serializers.CharField(label='country')

    def validate(self, data):
        code = data.get('code')
        email = data.get('email')
        user = User.objects.get(email=email)
        reg_profile = RegistrationProfile.objects.get(code=code)
        if reg_profile != user.registration_profile:
            raise ValidationError(message='The code does not belong to this email!')
        if data.get('password') != data.get('password_repeat'):
            raise ValidationError(message='Passwords do not match!')
        return data

    def save(self, validated_data):
        email = validated_data.get('email')
        user = User.objects.get(email=email)
        user.first_name = validated_data.get('first_name')
        user.last_name = validated_data.get('last_name')
        user.is_active = True
        user.set_password(validated_data.get('password'))
        user.registration_profile.code_used = True
        user.save()
        user.registration_profile.save()
        # Creating user profile here and not with signal because I need to set
        # the user's phone number
        user_profile = UserProfile(
            user=user,
            phone_number=validated_data.get('phone_number'),
            country=validated_data.get('country')
        )
        user_profile.save()
        # If the user is registering because they were invited to an Existing Group
        # This adds them to the group, removes them as being an Invited User and
        # emails them they were added to a new Group
        if user.registration_profile.inviting_group:
            target_group = Group.objects.get(id=user.registration_profile.inviting_group.id)
            user.user_profile.groups.add(target_group)
            user.registration_profile.inviting_group = None
            user.registration_profile.save()
        notify_users.send(sender=User, notification_key='new_user_registered', request=self.context['request'], email=user.email)
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(label='Password Reset E-Mail Address', validators=[email_does_exist])

    def validate(self, data):
        email = data.get('email').lower()
        user = User.objects.get(email=email)
        if not user.is_active:
            raise ValidationError(message="This user didn't sign up yet!")
        return data

    def send_password_reset_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.registration_profile.code = code_generator()
        user.registration_profile.code_used = False
        user.registration_profile.code_type = 'PR'
        user.registration_profile.save()
        send_email.send(sender=User, request=self.context['request'], to=email, email_type='password_reset_email', code=user.registration_profile.code)


class PasswordResetValidationSerializer(serializers.Serializer):
    code = serializers.CharField(label='Validation code', write_only=True, validators=[code_is_valid])
    email = serializers.EmailField(label='Registration E-Mail Address', validators=[email_does_exist])
    password = serializers.CharField(label='password', write_only=True)
    password_repeat = serializers.CharField(label='password_repeat', write_only=True)

    def validate(self, data):
        code = data.get('code')
        email = data.get('email')
        user = User.objects.get(email=email)
        reg_profile = RegistrationProfile.objects.get(code=code)
        if reg_profile != user.registration_profile:
            raise ValidationError(message='The code does not belong to this email!')

        if data.get('password') != data.get('password_repeat'):
            raise ValidationError(message='Passwords do not match!')
        return data

    def save(self, validated_data):
        code = validated_data.get('code')
        user = RegistrationProfile.objects.get(code=code).user
        user.set_password(validated_data.get('password'))
        user.registration_profile.code_used = True
        user.save()
        user.registration_profile.save()
        post_user_password_reset_validation.send(sender=User, user=user)
        notify_users.send(sender=User, notification_key='user_reset_password', request=self.context['request'], email=user.email)
        return user
