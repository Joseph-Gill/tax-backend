# Social Media App
This apps groups all functionality related to posts, comments, and friends.
#### Prerequisites
1. A User Model on which many to many rels are defined.
#### Installation & Usage
1. Install the app
```
INSTALLED_APPS = [
    ...
    'app.social',
    ...
]
```
2. Add
 ```
path('backend/api/social/', include('app.social.urls')),
``` 
to your root urls.py to have access to all registration endpoints.
