import django.dispatch

post_user_project_creation = django.dispatch.Signal(providing_args=["user_profile", "new_project"])
