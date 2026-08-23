from django.db import models
from django.utils.text import slugify
from django.urls import reverse



class Genre(models.Model):
    genre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='genre_icons/',null=True,blank=True)

    def __str__(self):
        return self.genre
    
    def get_genre_wise_products_url(self):
        return reverse('genre-wise-books', args=[self.slug])
    
#model for Book

class Book(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True,blank=True)
    author  = models.CharField(max_length=150)
    short_description = models.TextField()
    price = models.IntegerField(null=True,blank=True)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='book_images/',null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title

    def get_book_url(self):
        return reverse('single-book',args=[self.genre.slug, self.slug])
