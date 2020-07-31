# Social Auth
This app includes social authentication backends for Google and LinkedIn.


#### Prerequisites
1. A User Model
2. A Registration Model
3. A Social Profile Model


#### Installation & Usage
1.Install the app in settings.py
```
INSTALLED_APPS = [
    ...
    'app.social_auth',
    ...
]
```

2. Add needed custom backends in settings.py
```
AUTHENTICATION_BACKENDS = (
    # Custom
    'app.social_auth.backends.GoogleOpenIdBackend',
    'app.social_auth.backends.LinkedinOAuth2Backend',
    # Django
    'django.contrib.auth.backends.ModelBackend',
)
```
The order matters! Put the custom backends first.


## How it works in general
1. In the frontend, users are redirected to social login pages from the respective platform to receive things like permissions, id_token etc.
2. The frontend sends a request to this Django backend with the needed data (token etc.) and and argument as of which platform it is from (for ex. 'googleOpenId').
3. Djangos AuthenticationMiddleware will go through the list in AUTHENTICATION_BACKENDS until it finds the backend corresponding to the argument passed in step 2. If it doesn't find any match, it will use the ModelBackend.
4. Some verification steps are needed depending on the platform and then the user information like email, firstName etc. can be retrieved.
5. Based on the email, we check if the user already exists. Else, a new user is created.
6. A JWT token is created with this Django backend and sent to the frontend.


## How it works with Google

1. Create and configure a new project to get Google OAuth2 Key and Secret on [Google Developer Console](https://console.developers.google.com/)
<br>In the template we have configured that only people within our organization can login (...@propulsionacademy.com)
<br>
<br>
**Frontend**
2. On Google login request, the auth2 library needs to be loaded from gapi and a GoogleAuth session needs to be initialized, by passing the Google OAuth client_id/key from step 1.
3. The method signIn on googleAuth needs to be called, which will open a new window where the user can select his google account / login with google credentials.
4. Through googleAuth you now have to retrieve the currentUser to get his id_token. This id_token needs to be sent to this Django backend.
<br>
<br>
**Backend**
5. The id_token needs to be verified with google's provided api endpoint, which will also return the user information.
6. Now you have access to the email and other data. You can find and return the existing user or create and return a new user.
7. The SocialTokenConvertSerializer will use the returned user from step 6 to get a JWT from this Django backend and return it to your frontend.

### Docs

[Google Sign-In Integration Docs](https://developers.google.com/identity/sign-in/web/sign-in)  
[Google Sign-In API Docs - gapi](https://developers.google.com/identity/sign-in/web/reference)  
[Google Developer Console](https://console.developers.google.com/)


## How it works with LinkedIn

1. Create and configure a LinkedIn application to get a Client ID and Client Secret on [LinkedIn Developer tools](https://www.linkedin.com/developers/apps/) 
<br>
<br>
**Frontend**
2. On LinkedIn login request, your application redirects the user to LinkedIn's OAuth 2.0 authorization page, where the member authenticates and grants permission to your app. 
3. LinkedIn's redirects your user to your defined redirect url and adds an authorization code via URL params.
4. Your frontend application sends a request to this Django backend with the authorization code.
<br>
<br>
**Backend**
5. With the authorization code you have to send another request to LinkedIn to retreive an accessToken.
6. With this access token, the user data like email, firstName etc. can be retreived from LinkedIn. With the retreived email, you can find and return the existing user or create and return a new user.
7. The SocialTokenConvertSerializer will use the returned user from step 6 to get a JWT from this Django backend and return it to your frontend.

### Docs

[LinkedIn Auth Flow Docs](https://docs.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow)  
[LinkedIn Developer tools](https://www.linkedin.com/developers/apps/)
