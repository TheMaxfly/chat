from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    #path('', views.index, name='index'),  # Vue pour l'URL racine
    path('', views.advisor_list, name='advisor_list'),
    path('start_conversation/<int:advisor_id>/', views.start_conversation, name='start_conversation'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
]


from django.contrib.auth.models import User