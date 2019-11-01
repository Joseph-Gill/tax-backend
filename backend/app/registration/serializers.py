from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers
from app.registration.models import Email
from app.users.models import code_generator

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


def code_is_valid(code):
    try:
        User.objects.get(code=code)
        return code
    except User.DoesNotExist:
        raise ValidationError(message='This code is not valid! It might already have been used.')


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(label='Registration E-Mail Address', validators=[email_does_not_exist])

    def save(self, validated_data):
        email = validated_data.get('email')
        new_user = User.objects.create_unvalidated_user(
            username=email,
            email=email,
            is_active=False,
        )
        new_user.save()
        email = Email(to=email, subject='Thank you for registering!',
                      content=f'Here is your validation code: {new_user.code}')
        email.save(request=self.context['request'])
        return new_user


class RegistrationValidationSerializer(serializers.Serializer):
    email = serializers.EmailField(label='Registration E-Mail Address', validators=[email_does_exist])
    code = serializers.CharField(label='Validation code', write_only=True, validators=[code_is_valid])
    password = serializers.CharField(label='password', write_only=True)
    password_repeat = serializers.CharField(label='password_repeat', write_only=True)
    first_name = serializers.CharField(label='First name')
    last_name = serializers.CharField(label='Last name')

    def validate(self, data):
        if data.get('password') != data.get('password_repeat'):
            raise ValidationError(message='Passwords do not match!')
        return data

    def save(self, validated_data):
        code = validated_data.get('code')
        user = User.objects.get(code=code)
        user.first_name = validated_data.get('first_name')
        user.last_name = validated_data.get('last_name')
        user.is_active = True
        user.set_password(validated_data.get('password'))
        user.code = code_generator()
        user.save()
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(label='Password Reset E-Mail Address', validators=[email_does_exist])

    def send_password_reset_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        email = Email(to=email, subject='Password reset',
                      content=f'Here is your password reset code: {user.code}')
        email.save(request=self.context['request'])


class PasswordResetValidationSerializer(serializers.Serializer):
    code = serializers.CharField(label='Validation code', write_only=True, validators=[code_is_valid])
    password = serializers.CharField(label='password', write_only=True)
    password_repeat = serializers.CharField(label='password_repeat', write_only=True)

    def validate(self, data):
        if data.get('password') != data.get('password_repeat'):
            raise ValidationError(message='Passwords do not match!')
        return data

    def save(self, validated_data):
        code = validated_data.get('code')
        user = User.objects.get(code=code)
        user.set_password(validated_data.get('password'))
        user.code = code_generator()
        user.save()
        return user
