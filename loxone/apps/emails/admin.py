from django.contrib import admin

from loxone.apps.emails.models import Email
from loxone.core.admin import BaseAdmin


class EmailAdmin(BaseAdmin):
    list_display = (
        "recipients",
        "sent",
    )
    list_filter = ("sent",)

    def get_queryset(self, request):
        return Email.all_objects.all()


admin.site.register(Email, EmailAdmin)
