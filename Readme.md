# Django Social Media Backend Template
1.To see and test all endpoints use the postman collection included in /backend.

2.This template is already set up for email sending. All the email related code is in the registration app.
You can easily extract it from there if you only need email sending for other projects.

3.Nginx is included in this template for convenience  but should probably be put in its own repo in a proper deployment.

4.This template uses a custom User model with email as the unique auth field.

Missing:
Friends,
Liking Comments,
Think about pro/cons still having a user profile in the social app:

Option1: Social Profile
Pro: Makes the social app more modular. Can be Used with any User model.
Con: Makes the code more complicated + nested Serializer

Option2: No Profile
Pro: Simpler and clearer code.
Con: Coupling between User and the Social app

Option3: Profile + change user in request object + Related managers
Pro: Social app decoupled from User and simple code

Todos:
Move token endpoint to user.
Add Reg Profile to Reg app.

Add Social Profile.
Move follower enpoints to social app.
