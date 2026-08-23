from django.contrib import admin
from .models import *



class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
admin.site.register(Book,BookAdmin)

class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('genre',)}

admin.site.register(Genre,GenreAdmin)

