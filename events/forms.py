from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone']
        labels = {
            'name': 'Ваше ФИО',
            'email': 'Email',
            'phone': 'Телефон',
        }
