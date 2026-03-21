from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['travel_date', 'num_adults', 'num_children', 'special_requests']
        widgets = {
            'travel_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'num_adults': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'num_children': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special requirements...'}),
        }
