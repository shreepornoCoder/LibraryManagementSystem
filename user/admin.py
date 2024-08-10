from django.contrib import admin
from .models import UserModel, BorrowBook

# Register your models here.
admin.site.register(UserModel)
admin.site.register(BorrowBook)