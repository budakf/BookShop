from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    phone = models.CharField(max_length=15)
    address = models.TextField('Address')

    def __str__(self):
        return self.user.username
    
class Writer(models.Model):
    first_name = models.CharField(max_length=80)
    last_name  = models.CharField(max_length=80)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Book(models.Model):
    book_name = models.CharField(max_length=80)
    book_writer = models.ManyToManyField(Writer,related_name='writers')
    book_published_date = models.DateField(default=now())
    book_price = models.DecimalField(max_digits=6, decimal_places=3)
    book_detail = models.TextField()

    def __str__(self):
        return self.book_name


class Cart(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=1)
    books = models.ManyToManyField(Book, related_name='books')

    def __str__(self):
        return self.owner.username

