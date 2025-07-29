from django.contrib import admin
from .models import Product, Variation, VariationCategory
from django.utils.translation import gettext_lazy as _
from django.utils import timezone  # Make sure to import timezone

class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1  # Number of empty forms to display
    fields = ['category', 'value', 'is_active']  # Display fields of variation in admin
    readonly_fields = ['category', 'value']  # Make fields read-only to avoid incorrect changes

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'is_available', 'created_date')
    list_display_links = ('product_name',)
    list_editable = ('price', 'stock', 'is_available')
    search_fields = ('product_name', 'description')
    list_filter = ('category', 'is_available', 'created_date')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [VariationInline]  # Show variations inline with product

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'category', 'value', 'is_active', 'created_date', 'modified_date')  # Fields to display in the list
    list_filter = ('category', 'is_active', 'product')  # Filters for the list
    search_fields = ('product__product_name', 'category__name', 'value')  # Search fields in admin
    list_editable = ['is_active']  # Allow direct editing of 'is_active' in the list
    ordering = ('product',)  # Default ordering by product
    # inlines = [VariationInline]  # Show variations inline when editing products
    fieldsets = (
        (None, {
            'fields': ('product', 'category', 'value', 'is_active')
        }),
        (_('Dates'), {
            'fields': ('created_date', 'modified_date'),
            'classes': ('collapse',)  # Collapse date fields to keep the form clean
        }),
    )
    readonly_fields = ('created_date', 'modified_date')  # Make these fields read-only

    def save_model(self, request, obj, form, change):
        if not obj.created_date:  # If created_date is not set, assign the current date and time
            obj.created_date = timezone.now()
        obj.save()

class VariationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Display name and description of the category
    search_fields = ('name', 'description')  # Search by name and description

# Register the models in the admin panel
admin.site.register(Product, ProductAdmin)
admin.site.register(VariationCategory, VariationCategoryAdmin)
admin.site.register(Variation, VariationAdmin)
