from django import forms
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import *


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','password1','password2','email')
       

    def save(self, commit: bool = True ):
        user = super(RegisterUserForm, self).save(commit=False)
        # user.instance.cashier = self.request.user
        if commit:
            user.save()
        return user
    
    def __init__(self,*args, **kwargs):
        super(RegisterUserForm,self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs['class'] = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        self.fields["username"].widget.attrs['placeholder'] = 'User name'

        self.fields["first_name"].widget.attrs['class'] = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        self.fields["first_name"].widget.attrs['placeholder'] = 'Tonks'

        self.fields["last_name"].widget.attrs['class'] = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        self.fields["last_name"].widget.attrs['placeholder'] = 'Dex'

        self.fields["email"].widget.attrs['class'] = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        self.fields["email"].widget.attrs['placeholder'] = 'dex_tonks@gmail.com'

        self.fields["password1"].widget.attrs['class'] = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"

        self.fields["password2"].widget.attrs['class'] = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        'block mb-2 text-sm font-medium text-gray-900 dark:text-white'
    
class CreateAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ('created_at','id')
        widget = {
            "date_of_birth":forms.DateInput(attrs=dict(type='date'))
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        # fields = '__all__'
        exclude = ('created_at',)
