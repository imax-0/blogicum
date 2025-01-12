from django.contrib import admin

from .models import Category, Location, Post, Comment

admin.site.empty_value_display = 'Не задано'


class PostInline(admin.StackedInline):
    model = Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'is_published'
    )
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = (
        'is_published',
        'slug'
    )
    inlines = (
        PostInline,
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published'
    )
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('is_published',)
    inlines = (
        PostInline,
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = (
        'title',
        'pub_date',
        'is_published',
        'author',
        'location',
        'category'
    )
    list_editable = (
        'pub_date',
        'is_published',
        'category'
    )
    search_fields = ('title',)
    list_filter = (
        'is_published',
        'category',
        'location'
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'is_published',
        'author'
    )
    list_editable = (
        'is_published',
    )
    list_filter = (
        'is_published',
    )
