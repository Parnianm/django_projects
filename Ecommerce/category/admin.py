from django.contrib import admin
from django.utils.html import format_html
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug', 'category_image_tag')
    prepopulated_fields = {'slug': ('category_name',)}
    search_fields = ('category_name',)
    readonly_fields = ('category_image_tag',)

    def category_image_tag(self, obj):
        if obj.category_image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 5px;" />', obj.category_image.url)
        return "-"
    category_image_tag.short_description = 'Image Preview'
