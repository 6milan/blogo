from django.contrib import admin
from .models import Comment, Post, Media, Category, Product, Event, Ad, Reply

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active', 'reply_to')  # Add 'reply_to' field here
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

class ReplyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'active', 'body', 'created_on')  
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')

    def approve_replies(self, request, queryset):
        queryset.update(active=True)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'status', 'display_category')
    list_filter = ('created_at', 'status', 'category')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}

    def display_category(self, obj):
        return obj.category

    display_category.short_description = 'Category'

    raw_id_fields = ('author',)
    filter_horizontal = ('media',)

class CategoryAdmin(admin.ModelAdmin):
    pass

class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'media_type', 'file')

class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_downloadable')

admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Event)
admin.site.register(Ad, AdAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Media, MediaAdmin)