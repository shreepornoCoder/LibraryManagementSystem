from django.contrib import admin
from django.urls import path, include
from .views import BookCreateView, BookDetailsView

urlpatterns = [
    path('add_books/', BookCreateView.as_view(), name="add_book"),
    path('details/<int:id>/', BookDetailsView.as_view(), name="book_detail")
]