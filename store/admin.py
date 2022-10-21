from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'created_at', 'quantity', 'price', 'discount','category', 'get_photo')
    list_editable = ('price', 'discount', 'quantity')
    list_display_links = ('title', )
    inlines = [GalleryInline]
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'price')

    def get_photo(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="75">')
            except:
                return '-'
        else:
            return '-'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_products_count')
    prepopulated_fields = {'slug': ('title',)}

    def get_products_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return '0'

    get_products_count.short_description = 'Tovarlar soni'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'product', 'text', 'created_at', 'publish')
    list_display_links = ('pk', 'text')
    readonly_fields = ('author', 'product', 'text', 'created_at')
    list_editable = ('publish', )

admin.site.register(Order)
