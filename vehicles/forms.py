from django import forms
from .models import CarBooking, AirportTransfer


class CarBookingForm(forms.ModelForm):
    class Meta:
        model = CarBooking
        fields = ['pickup_location', 'drop_location', 'pickup_date', 'return_date', 'special_requests']
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }


class AirportTransferForm(forms.ModelForm):
    class Meta:
        model = AirportTransfer
        fields = [
            'transfer_type', 'airport_name', 'flight_number',
            'passenger_name', 'passenger_phone', 'passenger_email',
            'pickup_address', 'drop_address',
            'pickup_date', 'pickup_time',
            'return_date', 'return_time',
            'passengers', 'luggage_count', 'vehicle_type', 'special_requests',
        ]
        widgets = {      
            'pickup_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
            'pickup_time': forms.TimeInput(attrs={'type': 'time'}),
            'return_time': forms.TimeInput(attrs={'type': 'time'}),
            'pickup_address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Full pickup address'}),
            'drop_address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Full drop address'}),
            'special_requests': forms.Textarea(attrs={'rows': 2}),
        }

    def clean(self):
        cleaned = super().clean()
        transfer_type = cleaned.get('transfer_type')
        return_date = cleaned.get('return_date')
        return_time = cleaned.get('return_time')
        if transfer_type == 'both':
            if not return_date:
                self.add_error('return_date', 'Return date is required for both pickup & drop.')
            if not return_time:
                self.add_error('return_time', 'Return time is required for both pickup & drop.')
        return cleaned
