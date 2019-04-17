from django.contrib import admin
from .models import Thread, Comment, Activity

class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title','created_at']
    search_fields = ['title','text','user__email','user__name']
    prepopulated_fields = {'slug': ['title']}


class CommentAdmin(admin.ModelAdmin):
    list_display = ['thread','user', 'created_at']
    search_fields = ['text','thread__title','user__name','user__email']


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Activity)