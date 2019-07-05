from django.contrib import admin
from .models import Book, Cart, Writer

# Register your models here.

class WriterAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    list_display_links = list_display


class BookAdmin(admin.ModelAdmin):
    list_display = ['book_name', 'book_price', 'book_published_date']
    list_display_links = list_display


class CartAdmin(admin.ModelAdmin):
    list_display = ["getUsername", "getBooks"]
    list_display_links = ["getUsername", "getBooks"]

    def getUsername(self, object):
        return object.owner.username


    def getBooks(self, object):
        if object.books.exists():
            return object.books.all()[0].book_name + " ..."
    
    getUsername.short_description = "Username"
    getBooks.short_description = "Books"


admin.site.register(Book, BookAdmin)
admin.site.register(Writer, WriterAdmin)
admin.site.register(Cart, CartAdmin)


