from django.contrib import admin
from . import models
from django.utils.html import format_html
class ProductImageInLine(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']
    fields = ['images', 'thumbnail']
    def thumbnail(self,instance):
        if instance.images.name!='':
            return format_html(f'<img src = "{instance.images.url}" class = thumbnail>')
        return ' '