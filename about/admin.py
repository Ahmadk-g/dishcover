from django.contrib import admin
from .models import About, CollaborateRequest
from django_summernote.admin import SummernoteModelAdmin


# Admin configuration for the About model, using Summernote for rich text editing
@admin.register(About)
class AboutAdmin(SummernoteModelAdmin):
    # Enable the Summernote editor for the 'content' field
    summernote_fields = ('content',)


# Admin configuration for the CollaborateRequest model
@admin.register(CollaborateRequest)
class CollaborateRequestAdmin(admin.ModelAdmin):
    # Display the 'message' and 'read' fields in the list view
    list_display = ('message', 'read',)