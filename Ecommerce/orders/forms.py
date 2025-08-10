from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'phone', 'email',
            'address_line_1', 'address_line_2', 'country',
            'state', 'city', 'order_note'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 1'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 2 (optional)'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'order_note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Order Note (optional)', 'rows': 3}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone': 'Phone Number',
            'email': 'Email',
            'address_line_1': 'Address Line 1',
            'address_line_2': 'Address Line 2',
            'country': 'Country',
            'state': 'State',
            'city': 'City',
            'order_note': 'Order Note',
        }
        error_messages = {
            'first_name': {
                'required': 'Please enter your first name.'
            },
            'last_name': {
                'required': 'Please enter your last name.'
            },
            'phone': {
                'required': 'Please enter your phone number.'
            },
            'email': {
                'required': 'Please enter your email address.',
                'invalid': 'Enter a valid email address.'
            },
            'address_line_1': {
                'required': 'Please enter your address.'
            },
            'country': {
                'required': 'Please enter your country.'
            },
            'state': {
                'required': 'Please enter your state.'
            },
            'city': {
                'required': 'Please enter your city.'
            },
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) < 8:
            raise forms.ValidationError("Phone number is too short.")
        return phone
