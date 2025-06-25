from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from django.shortcuts import get_object_or_404

@api_view(["GET"])
def api_books_list(request):
    books = Book.objects.all()  # obtenemos todos los libros
    serializer = BookSerializer(books, many=True)  # los convertimos a JSON
    return Response(serializer.data)  # devolvemos la respuesta con la info

@api_view(['GET'])
def api_get_book_by_id(request, id):
    book = get_object_or_404(Book, pk=id)
    serializer = BookSerializer(book)
    return Response(serializer.data)

@api_view(['GET'])
def api_get_books_by_genre(request, genre):
    books = Book.objects.filter(genre__name__iexact=genre)#utilizamos filter en lugar de get ya que esperamos que devuelva más de un objeto, utilizamos genre__name (modelo + campo que queremos buscar) y __iexact (para ignorar mayúsculas o minúsculas)
    serializer = BookSerializer(books, many=True)#many=True se debe añadir obligatoriamente a la hora de serializar listas, del mismo modo que usamos filter, es una forma de indicarle a django que estamos trabajando con una lista de objetos
    return Response(serializer.data)

@api_view(['GET'])
def api_get_books_by_subgenre(request, subgenre):
    books = Book.objects.filter(subgenre__name__iexact=subgenre)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_get_books_by_language(request, language):
    books = Book.objects.filter(language__iexact=language)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)