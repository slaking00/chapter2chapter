from rest_framework import serializers
from .models import Book, Author, Genre, Subgenre, Publisher



class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'country']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        #fields = 'name'
        fields = ['name'] #es importante añadirlo entre corchetes aunque sea solo un campo para que lo trate como una tupla y no como un string, del contrario dará error

class SubgenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subgenre
        #fields = 'name'
        fields = ['name']

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['name', 'country']

class BookSerializer(serializers.ModelSerializer):

    author = AuthorSerializer()
    genre = GenreSerializer()
    subgenre = SubgenreSerializer()
    publisher = PublisherSerializer()
    class Meta: 
        model = Book
        fields = '__all__'