from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Product, ShopOwner


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ShopOwnerForm(forms.ModelForm):
    class Meta:
        model = ShopOwner
        fields = ['shop_name', 'shop_address', 'shop_phone_number']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['shop_owner', 'name', 'description', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'description': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'price': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'shop_owner': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
        }
