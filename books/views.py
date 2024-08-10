#importing CBV's
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import Book_Form, CommentForms
from .models import Book

class BookCreateView(CreateView):
    model = Book
    template_name = 'add_book.html'
    form_class = Book_Form
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        messages.success(self.request, "New book added successfully!")    
        return super().form_valid(form)

class BookDetailsView(DetailView):
    model = Book
    pk_url_kwarg = 'id'
    template_name = 'book_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object 
        comments = post.comments.all()
        comment_form = CommentForms()

        context['comments'] = comments
        context['comment_form'] = comment_form
        context['post'] = post
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        comment_form = CommentForms(data=self.request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post 
            new_comment.save()

        return self.get(request, *args, **kwargs)


