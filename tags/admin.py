from django.contrib import admin
from .models import Tag,TaggedItem
# Register your models here.

@admin.register(Tag)
class TadAdmin(admin.ModelAdmin):
    search_fields = ['label__istartswith']