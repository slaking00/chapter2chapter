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

    @action(detail=False, methods=["get"], url_path="by-genre")
    def get_books_by_genre(self, request):
        genre = request.query_params.get("genre", "").strip().lower()

        # comprobamos primero que exista el género en la BBDD
        genre_obj = get_object_or_404(
            Genre, name__iexact=genre
        )  # buscamos directamente en el modelo

        # utilizamos filter en lugar de get ya que esperamos que devuelva más de un objeto, utilizamos genre__name (modelo + campo que queremos buscar) y __iexact (para ignorar mayúsculas o minúsculas)
        books = Book.objects.filter(genre__name__iexact=genre_obj.name)# cuando utilizamos filter, espera recibir un valor entero (string o integer, con lo cual hay que añadir el atributo especifico esperado porque sino recibe el objeto completo y da error, en este caso añadimos .name)

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

    @action(detail=False, methods=["get"], url_path="by-subgenre")
    def get_books_by_subgenre(self, request):
        subgenre = request.query_params.get("subgenre", "").strip().lower()
        subgenre_obj = get_object_or_404(Subgenre, name__iexact=subgenre)

        books = Book.objects.filter(subgenre__name__iexact=subgenre_obj.name)

        if not books.exists():
            return Response(
                {"error": "No books found with that subgenre."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="by-language")
    def get_books_by_language(self, request):
        lang = request.query_params.get("lang", "").strip().lower()

        code = self.LANGUAGE_MAP.get(lang)

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

    @action(detail=False, methods=["get"], url_path="by-format")
    def get_books_by_format(self, request):
        format_type = request.query_params.get("format_type", "").strip().lower()
        code = self.FORMAT_MAP.get(format_type.lower())

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

    @action(detail=False, methods=["get"], url_path="by-title")
    def get_books_by_title(self, request):
        title = request.query_params.get("title", "").strip().lower()
        books = Book.objects.filter(
            title__icontains=title
        )  # para facilitar la búsqueda al usuario utilizamos icontains en lugar de iexact ya que es más flexible

        if not books.exists():
            return Response(
                {"error": "No books found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(
            books, many=True
        )  # contemplamos la posibilidad de que existan libros con el mismo título, de ahí el many=True
        return Response(serializer.data)

    @action(
        detail=False, methods=["get"], url_path="by-publisher"
    )
    def get_books_by_publisher(self, request):
        publisher = request.query_params.get("publisher", "").strip().lower()
        publisher_obj = get_object_or_404(Publisher, name__iexact=publisher)

        books = Book.objects.filter(publisher=publisher_obj.name)

        if not books.exists():
            return Response(
                {"error": "No books found for that publisher."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="by-isbn")
    def get_book_by_isbn(self, request):
        isbn = request.query_params.get("isbn", "").strip().lower()
        book = get_object_or_404(Book, isbn__iexact=isbn)
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="by-author")
    def get_books_by_author(self, request):
        first_name = request.query_params.get("first_name", "").strip()
        last_name = request.query_params.get("last_name", "").strip()

        if not first_name and not last_name:
            return Response(
            {"error": "You must provide at least 'first_name' or 'last_name'."},
            status=status.HTTP_400_BAD_REQUEST,
        )

        filters = {}
        if first_name:
            filters["author__first_name__icontains"] = first_name
        if last_name:
            filters["author__last_name__icontains"] = last_name

        books = Book.objects.filter(**filters)

        if not books.exists():
            return Response(
            {"message": "No books found for the given author parameters."},
            status=status.HTTP_404_NOT_FOUND,
        )

        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

