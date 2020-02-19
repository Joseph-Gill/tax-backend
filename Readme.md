# Django DRF Backend Template

## Extending the template
1. Please make sure you keep the code style consistent when working on this project. If you are using an Intellij 
editor you can use the upload the `Propulsion.codestyle.json` to `Editor > Code Style > Python`  

2. Please keep the components of the project independent. Use signals for inter app communication as much as possible.

3. If you trigger new email or notification sending through the corresponding signals (which you have to since it's the Propulsion standard) you will have to add the new types to the db.
IF SOMEBODY ELSE USES THE CODE THEY WILL NOT HAVE THOSE ENTRIES IN THE DB!!. Therefore please keep the data migration files up to date.  

## Usage
### Thins you need to change
1.Change HOSTNAME to your hostname in the nginx conf file for deployment.

2.IMPORTANT!: Change the secret key in the prod.env or actually don't use a prod.env at all and inject all env variables 
you need from gitlab.

3.Change the sentry dsn in the env files.

4.To avoid crashed you need to define the email and notification types the paltform in the corresponding db model.
If you don't have them on the db the code will crash. You n 


### Misc
1.To see and test all endpoints use the postman collection included in /backend. Please keep it up to date!

2.This template feature 5 independent modules: users, email, registration, admin notifications and social.

3.Nginx is included in this template for convenience  but should probably be put in its own repo in a proper deployment.

4.This template uses a custom User model with email as the unique auth field.

5.The backend admin is hidden in a honeypot. Please change the true admin url to something else in the root urls.py.

6.This template is hooked up to Sentry (the error monitoring platform). Change the dsn address pointing to sentry in the .envs files. 

7.Emails are asynchronusly sent via celery. You can see the status of celery task in the django admin.

## Architecture

### Internal Services
- Backend
- DB
- Redis: JSON store.
- Celery: This container uses the same image as the db since celery needs to have access to the same code as the django code that delegates the tasks to it.
The tasks get stored in json format in the redis db. Thanks to a pip package yo can see celery tasks in the django admin. 
To create a new task you have to decorate the function with the appropiate decorator and call it.

### External Services
- Sentry: An error monitoring platform where you can see errors happening in production.

## Endpoints
All the following endpoints should be prefixed with /backend
#### Auth & Registration
* `/api/auth/token/` POST: Get a new JWT by passing username and password
* `/api/auth/token/refresh/` POST: Get a new JWT by passing an old still valid refresh token.
* `/api/auth/token/verify/` POST: Verify a token by passing the access token in the body
* `/api/registration/` POST: Register a new user by asking for an email (send email validation code)
* `/api/registration/validation/` PATCH: Validate a new registered user with a validation code sent by email
* `/api/auth/password-reset/` POST: Reset users password by sending a validation code in an email
* `/api/auth/password-reset/validation/` PATCH: Validate password reset token and set new password for the user

#### Users
	
* `/api/users/?search=<str:search_string>` GET: Get all the users or filter them by search string.
* `/api/users/<int:user_id>/` GET: Get specific user 
* `/api/users/me/` GET, PATCH, DELETE: Get logged in user 

#### Notifications
* `/api/notifications/` GET, POST: Get, create notification type.
* `/api/notifications/<int:pk>/` GET, PATCH, DELETE: Get, update, delete notification type.

#### Social
##### Social Profiles
* `/api/social/profile/?search=<str:search_string>` GET: Get all the social profiles or filter them by search string
* `/api/social/profile/<int:user_id>/` GET: Get specific social profile
* `/api/social/profile/me/` GET, PATCH, DELETE: Get, Update, Delete logged in users social profile

##### Follow
* `/api/social/toggle-follow/<int:social_profile_id>/` POST: Toggle following a social profile
* `/api/social/followers/followers/` GET: List of all the logged in user’s followers social profiles
* `/api/social/followers/following/` GET: List of all the social profiles the user is following


##### Friends
* `/api/social/friends/request/<int:social_profile_id>/` POST: Send friend request to another user
* `/api/social/friends/requests/<int:friend_request_id>/` GET,PATCH,DELETE: Get Update (Accept, Reject) or Delete an open friend request
* `/api/social/friends/requests/?status=<str:status>` GET: List of all friend requests logged in user is in  filtered by status
* `/api/social/friends/` GET: List all accepted friends¨

##### Posts
* `/api/social/posts/` GET,POST: user can make a new post by sending post data, or get all posts.
* `/api/social/posts/<int:post_id>/` GET, PATCH, DELETE: get a specific post by ID and display all the information about that post. Update or delete it if logged in user is the original poster
* `/api/social/posts/<int:social_profile_id>/?search=<str:search_string>` GET: lists all the posts of a specific user in chronological order
* `/api/social/posts/me/?search=<str:search_string>` GET: lists all the posts of logged in user.
* `/api/social/posts/following/?search=<str:search_string>` GET: lists all the posts of of users the logged in user is following.
* `/api/social/posts/friends/?search=<str:search_string>` GET: lists all the posts of of users the logged in user is following.
* `/api/social/posts/toggle-like/<int:post_id>/` POST: toggle like a post
* `/api/social/posts/likes/` GET: the list of the posts the user likes

##### Comments
* `api/social/comments/<int:post_id>/` GET, POST: Create new post or get all comments of a post.

