from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegistrationForm, UserUpdateForm, Deposit_Form
from django.views import View
from django.views.generic import TemplateView, FormView, CreateView, ListView, UpdateView
from books.models import Book
from .models import BorrowBook
from django.contrib.auth.mixins import LoginRequiredMixin

#for sending emails
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_deposit_email(user, amount, subject, template):
    message = render_to_string(template, {
        'user' : user,
        'amount' : amount 
    })

    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

def send_other_email(user, message, subject, template):
    message = render_to_string(template, {
        'user' : user,
        'message' : message
    })

    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


# Create your views here.
class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "authentication.html"
    success_url = reverse_lazy('homepage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "SignUp"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Signup Successful!")
        return super().form_valid(form)

class UserLoginView(LoginView): 
    template_name = "authentication.html"
    
    def get_success_url(self):
        send_other_email(self.request.user, "", "Account Creation", "acc_creation_email.html")
        return reverse_lazy("homepage")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Login"
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Login Successful!")
        return super().form_valid(form)
    
class UserLogoutView(LogoutView):
    def get_success_url(self):
        messages.success(self.request, "Logout Successful!")
        return reverse_lazy("homepage")
    
class UserUpdateProfileView(View):
    template_name = "authentication.html"

    def get(self, request):
        form = UserUpdateForm(instance = request.user)
        context = {
            "form": form,
            "type": "Update Your Profile"
        }
        return render(self.request, self.template_name, context=context)
    
    def post(self, request):
        form = UserUpdateForm(request.POST, instance = request.user)

        if form.is_valid:
            form.save()
            send_other_email(self.request.user, "", "Account Creation", "profile_update_email.html")
            return redirect("homepage")
        
        context = {
            "form": form,
        }
        return render(self.request, self.template_name, context)
    
class UserProfileView(TemplateView):
    template_name = "profile.html"
    model = BorrowBook
    context_object_name = "books"
    pk_url_kwarg = 'id'
    
    def post(self, request, id, *args, **kwargs):
        book_id = self.request.POST.get('book_id')
        book = get_object_or_404(Book, book_id = id)
        user = self.request.user.account

        if user.balance > 0 and user.balance >= book.price:
            user.balance -= book.price
            user.save(update_fields=['balance'])
            print("book buy")

            BorrowBook.objects.create(user=self.request.user, book=book, is_returned=False)
            #BorrowBook.book.save(update_fields=['is_reutrned'])

            messages.success(request, "Book borrowed successfully!")
        else:
            messages.error(request, "You don't have enough money!")

        return redirect('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        borrowed_books = BorrowBook.objects.filter(user=self.request.user)
        context["books"] = borrowed_books
        return context
    
class DepositView(FormView):
    form_class = Deposit_Form
    template_name = "deposit_money.html"
    success_url = reverse_lazy("profile") 

    def form_valid(self, form):
        amount = form.cleaned_data.get("amount")
        user_acc = self.request.user.account
        user_acc.balance += amount

        user_acc.save(
            update_fields=[
                'balance'
            ]
        )
        send_deposit_email(self.request.user, amount, "Money Deposit", "deposit_email.html")
        messages.success(self.request, f"{amount}$ Money has been Deposited Successfully to your account!")
        return super().form_valid(form)

class BorrowBookView(LoginRequiredMixin, ListView):
    pass 

class ReturnBook(View):
    # model = BorrowBook
    # pk_url_kwarg = 'id'
    # success_url = reverse_lazy("profile")

    def post(self, request, id, *args, **kwargs):
        borrow_instance = get_object_or_404(BorrowBook, id=id)
        user = request.user.account

        # Increase the user's balance by the price of the book they are returning
        user.balance += borrow_instance.book.price
        borrow_instance.is_returned = True
        user.save(update_fields=['balance'])
        borrow_instance.save(update_fields=['is_returned'])
        
        messages.success(request, "Book returned successfully!")
        return redirect('profile')