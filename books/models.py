from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Publisher(models.Model):
    name = models.CharField(unique=True, max_length=20)
    country = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name
    
class Subgenre(models.Model):
    name = models.CharField(unique=True, max_length=20)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Book(models.Model):

    FORMAT_CHOICES = [("PHY", "Physical"), ("EB", "E-Book")]

    LANGUAGE_CHOICES = [("SPA", "Spanish"), ("ENG", "English")]

    title = models.CharField(max_length=100)
    synopsis = models.TextField()
    pages = models.PositiveSmallIntegerField(validators=[MinValueValidator(50)])
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    cover = models.ImageField(upload_to="covers/")
    isbn = models.CharField(
        "ISBN",
        unique=True,
        max_length=17,
    )  # max_length será de 17 para almacenarlo con guiones
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    format_type = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publication_date = models.DateField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    subgenre = models.ForeignKey(Subgenre, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



