import copy

from rest_framework.permissions import DjangoModelPermissions

"""
User has to be in specific group to have any of the permissions including GET.
"""


class ViewDjangoModelPermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]
