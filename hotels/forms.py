from django import forms
from .models import HotelBooking, RoomType


class HotelBookingForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = ['room_type', 'check_in', 'check_out', 'num_rooms', 'num_guests', 'special_requests']
        widgets = {
            'room_type': forms.Select(attrs={'class': 'form-select'}),
            'check_in': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'num_rooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'num_guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, hotel=None, **kwargs):
        super().__init__(*args, **kwargs)
        if hotel:
            self.fields['room_type'].queryset = RoomType.objects.filter(hotel=hotel, is_available=True)
