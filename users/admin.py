from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.db.models.signals import post_save

from .models import User

UserModel = get_user_model()

admin.site.register(UserModel, UserAdmin)


def add_user_to_public_group(sender, instance, created, **kwargs):
    """Post-create user signal that adds the user to everyone group."""

    try:
        if created and instance.type:
            instance.groups.add(Group.objects.get(name=instance.type))
    except Group.DoesNotExist:
        pass


post_save.connect(add_user_to_public_group, sender=User)
