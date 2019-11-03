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
Current thoughts:
To decouple user from social app you need the user profile.
But this reintroduces the operational complexity I wanted to get rid of in the first place.
-> Probably better to have one template really just for social media app where we sacrifice modular 
independence and have the tight coupling and then just have another template without the social compoenntn.
