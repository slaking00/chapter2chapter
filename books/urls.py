from django.urls import path
from .views import api_books_list, api_get_book_by_id, api_get_books_by_genre, api_get_books_by_subgenre, api_get_books_by_language

urlpatterns = [
    path('api/all-books/', api_books_list),
    path('api/book-by-id/<int:id>', api_get_book_by_id),
    path('api/books-by-genre/<str:genre>', api_get_books_by_genre),
    path('api/books-by-subgenre/<str:subgenre>', api_get_books_by_subgenre),
    path('api/books-by-language/<str:language>', api_get_books_by_language)
]
