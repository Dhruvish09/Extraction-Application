from django.contrib import admin
from .models import Document, FailedUpload


@admin.register(FailedUpload)
class FailedUploadAdmin(admin.ModelAdmin):
    list_display = ('user', 'file_name', 'created_at')

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file', 'file_url', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username', 'file__name')
    ordering = ('-created_at',)


# Register the admin classes with their respective models
admin.site.register(Document, DocumentAdmin)
