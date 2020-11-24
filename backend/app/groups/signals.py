import django.dispatch

post_user_group_creation = django.dispatch.Signal(providing_args=["user_profile", "name", "new_group"])
