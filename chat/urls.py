from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('chat_window/', views.chat_window, name='chat_window'),
    path('advisor_list/', views.advisor_list, name='advisor_list'),
    path('start_conversation/<int:advisor_id>/', views.start_conversation, name='start_conversation'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('advisor_conversations/', views.advisor_conversations, name='advisor_conversations'),
]
