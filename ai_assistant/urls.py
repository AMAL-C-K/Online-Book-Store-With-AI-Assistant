from django.urls import path

from . import views

urlpatterns = [
    path("book/<int:book_id>/", views.book_chat_api, name="book_chat_api"),
    path("book/<int:book_id>/chat/clear", views.clear_book_chat, name="clear_book_chat"),
]
