from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserModel, DepositModel

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    widgets = {
        "first_name" : forms.TextInput(attrs={"id":"required"}),
        "last_name" : forms.TextInput(attrs={"id":"required"}),
        "email" : forms.EmailInput(attrs={"id":"required"})
    }

    def save(self, commit=True):
        our_user = super().save(commit=True)

        if commit == True:
            our_user.save()

            first_name = self.cleaned_data.get('first_name')
            last_name = self.cleaned_data.get('last_name')
            email = self.cleaned_data.get('email')

            UserModel.objects.create(
                user = our_user,
                first_name = first_name,
                last_name = last_name,
                email = email,
                balance = 0
            )
        
        return our_user
    
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            try:
                user_account = self.instance.account

            except UserModel.DoesNotExist:
                user_account = None

            if user_account:
                self.fields["first_name"].initial = user_account.first_name
                self.fields["last_name"].initial = user_account.last_name
                self.fields["email"].initial = user_account.email 

    def save(self, commit = True):
        user = super().save(commit=True)

        if commit:
            user.save()

            user_account, created = UserModel.objects.get_or_create(user = user)

            user_account.first_name = self.cleaned_data['first_name']
            user_account.last_name = self.cleaned_data['last_name']
            user_account.email = self.cleaned_data['email']

        return user 
    
class Deposit_Form(forms.ModelForm):
    class Meta:
        model = DepositModel
        fields = "__all__"