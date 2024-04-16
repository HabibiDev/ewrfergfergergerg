from django.contrib import admin
from .models import Category, ImagePost, Post
from mptt.admin import MPTTModelAdmin
from mptt.admin import TreeRelatedFieldListFilter


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    list_filter = (

        ('category', TreeRelatedFieldListFilter),
    )
    list_display = (
        'title',
        'category',
        'price',
        'created',
        'is_active')


admin.site.register(Category, MPTTModelAdmin)
admin.site.register(ImagePost)
