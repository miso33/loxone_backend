from django.contrib import admin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter

from loxone.apps.emails.models import Email
from loxone.core.admin import BaseAdmin


class EmailAdmin(BaseAdmin):
    list_display = (
        "recipients",
        "sent",
        "created"
    )
    list_filter = ("sent", ("created", DateTimeRangeFilter))

    def get_queryset(self, request):
        return Email.all_objects.all()


admin.site.register(Email, EmailAdmin)
