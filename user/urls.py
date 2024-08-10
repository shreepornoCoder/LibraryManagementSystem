from django.urls import path, include
from .views import RegistrationView, UserLoginView, UserLogoutView, UserUpdateProfileView, UserProfileView, DepositView, BorrowBookView, ReturnBook

urlpatterns = [
    path('signup/', RegistrationView.as_view(), name="signup"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', UserLogoutView.as_view(), name="logout"),
    path('profile/', UserProfileView.as_view(), name="profile"),
    path('update_profile/', UserUpdateProfileView.as_view(), name="profile_update"),
    path("deposit_money/", DepositView.as_view(), name="deposit_money"),
    path('borrow/<int:id>/', UserProfileView.as_view(), name="profile"), 
    path('return_book/<int:id>/', ReturnBook.as_view(), name="book_return"), 
]
