from rest_framework.viewsets import ModelViewSet
from books.models import Book, Genre, Subgenre, Author, Publisher
from api.serializers.book_serializers import BookSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

LANGUAGE_MAP = {"spanish": "SPA", "english": "ENG"}
FORMAT_MAP = {"physical": "PHY", "e-book": "EB"}

@action(detail=False, methods=["get"], url_path="by-genre/(?P<genre>[^/.]+)")
def api_get_books_by_genre(self, request, genre):
    # comprobamos primero que exista el género en la BBDD
    genre_obj = get_object_or_404(
        Genre, name__iexact=genre
    )  # buscamos directamente en el modelo

    # utilizamos filter en lugar de get ya que esperamos que devuelva más de un objeto, utilizamos genre__name (modelo + campo que queremos buscar) y __iexact (para ignorar mayúsculas o minúsculas)
    books = Book.objects.filter(genre__name__iexact=genre_obj)

    # comprobamos que existan libros con ese género
    if not books.exists():
        return Response(
            {"error": "No books found with that genre."},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = self.get_serializer(
        books, many=True
    )  # many=True se debe añadir obligatoriamente a la hora de serializar listas, del mismo modo que usamos filter, es una forma de indicarle a django que estamos trabajando con una lista de objetos
    return Response(serializer.data)


@action(detail=False, methods=["get"], url_path="by-subgenre/(?P<subgenre>[^/.]+)")
def api_get_books_by_subgenre(self, request, subgenre):
    subgenre_obj = get_object_or_404(Subgenre, name__iexact=subgenre)

    books = Book.objects.filter(subgenre__name__iexact=subgenre_obj)

    if not books.exists():
        return Response(
            {"error": "No books found with that subgenre."},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = self.get_serializer(books, many=True)
    return Response(serializer.data)



@action(detail=False, methods=['get'], url_path='by-language/(?P<lang>[^/.]+)')#utilizamos una regex para personalizar la URL y poder pasarle parámetros (que no contengan ni barras ni puntos, en este caso) que luego el método utilizará para realizar las validaciones pertinentes
def api_get_books_by_language(self, request, lang):

    code = LANGUAGE_MAP.get(lang.lower())

    if not code:
        return Response(
            {"error": "Language not supported"}, status=status.HTTP_404_NOT_FOUND
        )

    books = Book.objects.filter(language__iexact=code)

    if not books.exists():
        return Response(
            {"error": f"No books found in {lang}."},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = self.get_serializer(books, many=True)
    return Response(serializer.data)





@action(detail=False, methods=["get"], url_path="by-format/(?P<format_type>[^/.]+)")
def api_get_books_by_format(self, request, format_type):

    code = FORMAT_MAP.get(format_type.lower())

    if not code:
        return Response(
            {"error": "Format not supported"}, status=status.HTTP_404_NOT_FOUND
        )

    books = Book.objects.filter(format_type__iexact=code)

    if not books.exists():
        return Response(
            {"error": "No books found in that format."},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = self.get_serializer(books, many=True)
    return Response(serializer.data)


@action(detail=False, methods=["get"], url_path="by-title/(?P<title>[^/.]+)")
def api_get_books_by_title(self, request, title):
    books = Book.objects.filter(title__icontains=title) #para facilitar la búsqueda al usuario utilizamos icontains en lugar de iexact ya que es más flexible

    if not books.exists():
        return Response({"error": "No books found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = self.get_serializer(
        books, many=True
    )  # contemplamos la posibilidad de que existan libros con el mismo título, de ahí el many=True
    return Response(serializer.data)


@action(detail=False, methods=["get"], url_path="by-publisher/(?P<publisher>[^/.]+)")
def api_get_books_by_publisher(self, request, publisher):
    publisher_obj = get_object_or_404(Publisher, name__iexact=publisher)

    books = Book.objects.filter(publisher=publisher_obj)

    if not books.exists():
        return Response(
            {"error" : "No books found for that publisher."},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = self.get_serializer(books, many=True)
    return Response(serializer.data)


@action(detail=False, methods=["get"], url_path="by-isbn/(?P<isbn>[^/.]+)")
def api_get_book_by_isbn(self, request, isbn):
    book = get_object_or_404(Book, isbn__iexact=isbn)
    serializer = self.get_serializer(book)
    return Response(serializer.data)


@action(detail=False, methods=["get"], url_path="by-author/(?P<author>[^/.]+-[^/.]+)")
def api_get_books_by_author(self, request, author):
    try:
        first_name, last_name = author.split("-")
    except ValueError:
        return Response(
            {"error": "Author name must be in 'First-Last' format."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Comprobamos si el autor existe
    author_obj = get_object_or_404(
        Author, first_name__iexact=first_name, last_name__iexact=last_name
    )

    books = Book.objects.filter(author=author_obj)

    if not books.exists():
        return Response(
            {"message": "Author exists but has no books."}, status=status.HTTP_200_OK
        )
    
    serializer = self.get_serializer(books, many=True)
    return Response(serializer.data)



