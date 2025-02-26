from django.contrib import admin

# Register your models here.
# chat/admin.py

from django.contrib import admin
from .models import Profile, TemporaryConversation, Message

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_advisor')
    search_fields = ('user__username',)
    list_filter = ('is_advisor',)

class TemporaryConversationAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'advisor', 'created_at', 'expires_at')
    search_fields = ('name', 'client__username', 'advisor__username')
    list_filter = ('created_at', 'expires_at')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'content', 'timestamp')
    search_fields = ('conversation__name', 'sender__username', 'content')
    list_filter = ('timestamp',)    

admin.site.register(Profile)
admin.site.register(TemporaryConversation, TemporaryConversationAdmin)
admin.site.register(Message, MessageAdmin)
