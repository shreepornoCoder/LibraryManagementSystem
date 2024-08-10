from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from django.utils import timezone

# Create your models here.
class UserModel(models.Model):
    user = models.OneToOneField(to=User, related_name="account", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    balance = models.DecimalField(decimal_places=2, max_digits=12, default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class BorrowBook(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    borrowing_date = models.DateTimeField(auto_now_add=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} is borrowed by {self.user.username}"

class DepositModel(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=12)
