from django.contrib import admin
from .models import Post, Score, Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'created', 'status', 'avr_score')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body_text')

admin.site.register(Post, PostAdmin)
admin.site.register(Score)
admin.site.register(Comment)
