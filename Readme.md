# Django DRF Backend Template

## Run

1. Build the image

2. Set up pycharm with the docker-compose interpreter as explained in the curriculum.
	
3. Run the containers: `docker-compose up -d` and run the desired command from PyCharm.

    
## Extending the template
1. Please make sure you keep the code style consistent when working on this project. If you are using an Intellij 
editor you can use the upload the `Propulsion.codestyle.json` to `Editor > Code Style > Python`  

2. Please keep the components of the project independent. Use signals for inter app communication as much as possible.

3. If you trigger new email or notification sending through the corresponding signals (which you have to since it's the Propulsion standard) you will have to add the new types to the db.
IF SOMEBODY ELSE USES THE CODE THEY WILL NOT HAVE THOSE ENTRIES IN THE DB!!. Therefore please keep the data migration files up to date.  

## Usage
### Things you need to change
1.IMPORTANT!: Change the secret key in the prod.env or actually don't use a prod.env at all and inject all env variables 
you need from gitlab.

2.Change the sentry dsn in the env files.

3.To avoid crashed you need to define the email and notification types the paltform in the corresponding db model.
If you don't have them on the db the code will crash.  


### Misc
1.To see and test all endpoints use the postman collection included in /backend. Please keep it up to date!

2.This template feature 5 independent modules: users, email, registration, admin notifications and social.

3.This template uses a custom User model with email as the unique auth field.

4.The backend admin is hidden in a honeypot. Please change the true admin url to something else in the root urls.py.

5.This template is hooked up to Sentry (the error monitoring platform). Change the dsn address pointing to sentry in the .envs files. 

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
* `/api/users/groups/<int:group_id>/` GET: Get all users for a specified group

#### Notifications
* `/api/notifications/` GET, POST: Get, create notification type.
* `/api/notifications/<int:pk>/` GET, PATCH, DELETE: Get, update, delete notification type.

#### User Profiles
* `/api/userprofiles/me/` GET, PATCH: Get, update the logged-in user's profile
* `/api/userprofiles/tasks/me/` GET: Get all tasks assigned to logged-in user
* `/api/userprofiles/group/<int:group_id>/userprofile/<int:userprofile_id>/` PATCH: Update or remove a specified User's role for projects of a specified group

#### Organizations
* `/api/orgs/group/<int:group_id>/?search=<str:search_string>` GET, POST: Get all organizations or filter them by search string for a specified group, create a new organization for a specified group
* `/api/orgs/org/<int:org_id>/` GET, PATCH, DELETE: Get, update, delete a specified organization
* `/api/orgs/group/<int:group_id>/user/<int:user_id>/` GET: Get the organization shared by a specified user and specified group

#### Groups
* `/api/groups/?search=<str:search_string>` GET, POST: Get all groups or filter them by search string, create a new group, creating user is assigned to the group
* `/api/groups/group/<int:group_id>/user/` POST: Add a user to a specified group, triggers registration on new to app users
* `/api/groups/me/` GET: Get all groups of the logged-in user
* `/api/groups/group/<int:group_id>/` GET, PATCH, DELETE: Get, update, delete a specified group
* `/api/groups/group/<int:group_id>/removeusers/` DELETE: Delete a list of users from a specified group, and all that group's projects
* `/api/groups/project/<int:project_id>/` GET: Get the group a specified project belongs to
* `/api/groups/group/<int:group_id>/favorite/` POST: Toggle the favorite status of a specified group for the logged-in user
* `/api/groups/allandfavorite/` GET: Get all and favorite groups for the logged-in user

#### Projects
* `/api/projects/group/<int:group_id>/?search=<str:search_string>` GET, POST: Get all projects or filter them by search string, create a new Project for specified group
* `/api/projects/project/<int:project_id>/` GET, PATCH, DELETE: Get, update, delete a specified project
* `/api/projects/project/<int:project_id>/accessusers/` GET: List all user profiles with access to a specified project
* `/api/projects/project/<int:project_id>/complete/` PATCH: Set a specified project's start date, end date, and status as complete

#### Charts
* `/api/charts/project/<int:project_id>/stepnumber/<int:step_number>/createchart/` POST: Create a chart for a specified step
* `/api/charts/project/<int:project_id>/stepnumber/<int:step_number>/` GET, PATCH, DELETE: Get, update, delete a specified chart

#### Steps
* `/api/steps/project/<int:project_id>/` GET, POST: Get all or create a step for a specified project
* `/api/steps/step/<int:step_id>/` GET, PATCH, DELETE: Get, update, delete a specified step
* `/api/steps/project/<int:project_id>/statusnumbers/` GET: Get the status numbers of all steps of a specified project
* `/api/steps/project/<int:project_id>/firstuncompleted/` GET: Get the first uncompleted step for a specified project
* `/api/steps/step/<int:step_id>/completed/` PATCH: Updated and set a specified step as completed, updating the group entities and setting chart histories as no longer pending

#### Tasks
* `/api/tasks/<int:step_id>/` GET: Get all tasks for a specified step
* `/api/tasks/step/<int:step_id>/userprofile/<int:userprofile_id>/` POST: Create a new Task for a specified Step and User
* `/api/tasks/task/<int:task_id>/user/<int:user_id>/` POST: Update specified Task with a new specified User
* `/api/tasks/task/<int:task_id>/` GET, PATCH, DELETE: Get, update, delete a specified step
* `/api/tasks/project/<int:project_id>/` GET: Get all tasks for a specified project
* `/api/tasks/project/<int:project_id>/stepnumber/<int:step_number>/` GET: Get all tasks for specified step number of specified project
* `/api/tasks/project/<int:project_id>/user/uncompleted/` GET: Retrieve all uncompleted tasks for logged-in user for a specified project and how many tasks are past due for that user.
* `/api/tasks/task/<int:task_id>/step/<int:step_id>/tasknumber/` GET: Retrieve the task number of a specific task for a specific step

#### Tax Consequences
* `/api/taxes/step/<int:step_id>/` GET, POST: Get all or create a task consequence for a specified Step
* `/api/taxes/tax/<int:tax_id>/` GET, PATCH, DELETE: Get, update, delete a specified tax consequence, updating sets logged-in user as editing_user of tax consequence
* `/api/taxes/tax/<int:tax_id>/reviewed/` POST: Set the reviewed status of a specified tax consequence as true, reviewing_user is set as logged-in user
* `/api/taxes/tax/<int:tax_id>/notreviewed/` POST: Set the reviewed status of a specified tax as false
* `/api/taxes/project/<int:project_id>/notreviewed/samecountry/` GET: List all tax consequences that are not reviewed and for the same country as the logged-in user
* `/api/taxes/project/<int:project_id>/opencomments/toreviewcomments/` GET: Get the number of "open" and "not Reviewed" tax consequences of the logged-in user's country, for a specified project

#### Project Roles
* `/api/projectroles/userprofile/<int:userprofile_id>/group/<int:group_id>/` GET: Get all project roles for a specified user and group
* `/api/projectroles/group/<int:group_id>/project/<int:project_id>/` GET: Get all user project roles for a specified group and specified project
* `/api/projectroles/userprofile/<int:userprofile_id>/project/<int:project_id>/` POST: Toggle the favorite status of a specified project for a specified user profile

#### Task Documents
* `/api/taskdocuments/<int:taskdocument_id>/` DELETE: Delete specified task document

#### Entities
* `/api/entities/group/<int:group_id>/` POST: Create a new entity for a specified group

#### Entity Histories
* `/api/entityhistories/entity/<int:entity_id>/chart/<int:chart_id>/` POST: Create a new entity history for a specified entity and specified chart
* `/api/entityhistories/entity/<int:entity_id>/` GET: Get all histories for a specified entity that are not pending