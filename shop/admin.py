from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'status', 'featured', 'image_preview']
    list_filter = ['status', 'featured', 'category', 'created_at']
    search_fields = ['name', 'description', 'sku']
    list_editable = ['price', 'stock_quantity', 'status', 'featured']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'category')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'sku', 'stock_quantity', 'status')
        }),
        ('Media & Display', {
            'fields': ('image', 'image_preview', 'featured', 'rating')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'

    actions = ['make_active', 'make_inactive', 'make_featured']

    def make_active(self, request, queryset):
        queryset.update(status='active')
    make_active.short_description = "Mark selected products as active"

    def make_inactive(self, request, queryset):
        queryset.update(status='inactive')
    make_inactive.short_description = "Mark selected products as inactive"

    def make_featured(self, request, queryset):
        queryset.update(featured=True)
    make_featured.short_description = "Mark selected products as featured"
