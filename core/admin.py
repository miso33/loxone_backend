from import_export.admin import ImportExportModelAdmin


class BaseAdmin(ImportExportModelAdmin):
    list_display = ('status',)
    list_filter = ('status',)
    exclude = ('status_changed',)


class BaseRemovableAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ('is_removed',)
    list_filter = BaseAdmin.list_display + ('is_removed',)
