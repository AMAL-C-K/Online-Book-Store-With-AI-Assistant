from django.urls import path
from . import views
urlpatterns = [
    path('',views.all_books,name = 'all-books'),
    path('<slug:slug>', views.genre_wise_books, name = 'genre-wise-books'),
    path('<slug:genre_slug>/<slug:book_slug>', views.single_book, name = 'single-book'),
    path('search_book/', views.search_book, name = 'search-book')
]


