from django.urls import path
from .views import chat_view, chat_page

urlpatterns = [
    path('', chat_view, name='chat_view'),  
    path('chat-page/', chat_page, name='chat_page'),
    
]
