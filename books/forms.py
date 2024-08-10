from django import forms 
from .models import Book, Comment

class Book_Form(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ["isborrow", "isreturned", "book_id"]

    labels = {
        "title":"Book Title",
        "description":"Book Description",
        "price":"Price",
        "ratings":"Ratings",
        "image":"Image",
        "book_category":"Book Category"
    }

    widgets = {
        "title":forms.TextInput(attrs = {'placeholder':'Enter a book title', "rows":1}),
        "description":forms.TextInput(attrs = {'placeholder':'Enter book Description'}),
        "price":forms.TextInput(attrs = {'placeholder':'Enter book borrow price'}),
        "image":forms.TextInput(attrs = {'placeholder':'drop a image of the book'}),
    }

class CommentForms(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']