from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from books.models import Book, BookCategoryModel

def Home(request, category_slug=None):
    data = Book.objects.all()
    categories = BookCategoryModel.objects.all()

    if category_slug:
        category = get_object_or_404(BookCategoryModel, slug = category_slug)
        data = Book.objects.filter(book_category = category)

    return render(request, 'home.html', {"data":data, "category":categories})

