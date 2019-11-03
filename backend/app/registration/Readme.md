# Registration
This django app groups all endpoints needed to register, log in and reset password.
#### Installation & Usage
Prerequisites: An Email model you save your emails to, and associated module that takes care of the email sending.
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
