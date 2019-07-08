from django.contrib import admin
from .models import Book, Cart, Writer, Customer

# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['get_username','phone', 'address']
    list_display_links = list_display

    def get_username(self,object):
        return object.user.username


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


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Writer, WriterAdmin)
admin.site.register(Cart, CartAdmin)


