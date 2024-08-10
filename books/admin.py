from django.contrib import admin
from .models import Book, BookCategoryModel, Comment

# Register your models here.
admin.site.register(Book)
admin.site.register(BookCategoryModel)
admin.site.register(Comment)