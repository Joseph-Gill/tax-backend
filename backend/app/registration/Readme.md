# Registration
This django app groups all endpoints needed to register, log in and reset password.
#### Installation & Usage
1. Install the app
```
INSTALLED_APPS = [
    ...
    'app.registration',
    ...
]
```
2. Add
 ```
path('backend/api/auth/', include('app.registration.urls')),
``` 
to your root urls.py to have access to all registration endpoints.
#### Interface
##### Dependencies
1. An Email (import in serializers.py) model you save your emails to, and associated module that takes care of the email sending.
2. A User model with a Manager that supports creating unverified users.
3. A UserSerializer (import in views.py)
##### API
1. This module exposes a Signal `post_user_registration_validation`.
To listen to this signal do:
```
@receiver(post_user_registration_validation)
def handle_signal(sender, user, **kwargs):
    pass
```
2. This module exposes a Signal `post_user_password_reset_validation`.
To listen to this signal do:
```
@receiver(post_user_password_reset_validation)
def handle_signal(sender, user, **kwargs):
    pass
```
3. This module exposes a Signal `send_auth_email`.
To listen to this signal do:
```
send_auth_email.send(sender=User, request=self.context['request'], to=email, email_type='registration_email', code=reg_profile.code)

def send_auth_email(sender, request, to, email_type, code, **kwargs):
def handle_signal(sender, user, **kwargs):
    pass
```
This signal is used to send individual emails to users via celery.
