# Registration
This django app groups all endpoints needed to register, log in and reset password.
If you just want it for email functionality rename it to email and remove serializers.py, views.py and urls.py.
## Usage
Add this app to your project.
Migrate to create the Email model shipped with this app.
The views and serializers take care of everything included saving the emails that have to be sent out to the Email model.
#### Configurations
Prerequisites: A django project with drf and a custom user model that supports creating an unvalidated user in the manager.
Otherwise modify the registration endpoint to use your own logic.
1. Install and add to your requirements.yml file: 
```
pip install django-extensions
pip install django-fullurl
```
2. Install the app
```
INSTALLED_APPS = [
     ...
    'fullurl',
     ...
    'app.registration',
]
```
3.Make sure you have:
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
4.Add Email settings:
```
BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '***'
EMAIL_HOST_PASSWORD = '***'
DEFAULT_FROM_EMAIL = '***'
```
5. Add the following to the root urls.py file.
```
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```
6.Change the image sent with the email in the static folder.
7.Start a docker container with your full project in it running `python manage.py send_mail`.
```
version: '3'
services:
  email:
    image: "your_image"
    restart: always
    env_file:
      - ./database.env
    command: 'python manage.py send_mail'
    depends_on:
      - database
      - api
```
