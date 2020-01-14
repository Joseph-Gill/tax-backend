# Notifications
This django app provides out of the box functionality for and admin notification system.

You can define notification Types in the django admin and then subscribe admin or staff users to these notifications in their Notification Profile. 
When a notification signal is triggered all subscribed users will receive the corresponding email.

#### Installation & Usage
1. Install the app
```
INSTALLED_APPS = [
    ...
    'app.notifications',
    ...
]
```
#### Interface
1. This module exposes a signal `notify_users` defined in signals.py
This signal can be called from other apps to trigger notifications.
When raising the signal through `notify_users.send(sender=User, notification_key='new_user_registered', request=self.context['request'], email=user.email)`
you need to provide the name of the signal (defined in django admin) and any additional arguments that have to be injected into the html template that will be sent by email.
