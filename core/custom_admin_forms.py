from django import forms
from tours.models import TourPackage
from core.models import Destination, Testimonial
from hotels.models import Hotel
from vehicles.models import Vehicle
from blog.models import BlogPost, BlogCategory
from gallery.models import GalleryImage, GalleryCategory


class TourForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = ['title', 'slug', 'destination', 'tour_type', 'difficulty',
                  'description', 'highlights', 'duration_days', 'duration_nights',
                  'price_per_person', 'discounted_price', 'max_group_size',
                  'min_age', 'thumbnail', 'thumbnail_url', 'is_featured', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.Select(attrs={'class': 'form-select', 'id': 'id_destination'}),
            'tour_type': forms.Select(attrs={'class': 'form-select'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'highlights': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_nights': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_person': forms.NumberInput(attrs={'class': 'form-control'}),
            'discounted_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_group_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'thumbnail_url': forms.URLInput(attrs={'class': 'form-control', 'id': 'id_thumbnail_url', 'placeholder': 'Auto-filled or paste image URL'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'slug', 'country', 'state', 'description', 'image', 'is_popular']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_popular': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'slug', 'destination', 'stars', 'description', 'address',
                  'phone', 'email', 'image', 'amenities', 'check_in_time',
                  'check_out_time', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.Select(attrs={'class': 'form-select'}),
            'stars': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'amenities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'check_in_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'vehicle_type', 'model', 'capacity', 'price_per_day',
                  'price_per_km', 'image', 'features', 'is_ac', 'driver_included',
                  'is_available', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_day': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_km': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'features': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_ac': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'driver_included': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'slug', 'author', 'category', 'thumbnail', 'excerpt',
                  'content', 'tags', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['category', 'title', 'image', 'description', 'is_featured']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'location', 'message', 'rating', 'image', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rating': forms.Select(attrs={'class': 'form-select'},
                                   choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)]),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


from bookings.models import Booking
from hotels.models import HotelBooking
from vehicles.models import CarBooking


class TourBookingEditForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['travel_date', 'num_adults', 'num_children', 'total_amount',
                  'status', 'payment_status', 'special_requests']
        widgets = {
            'travel_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'num_adults': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_children': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class HotelBookingEditForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = ['check_in', 'check_out', 'num_rooms', 'num_guests',
                  'total_amount', 'status', 'special_requests']
        widgets = {
            'check_in': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'num_rooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_guests': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CarBookingEditForm(forms.ModelForm):
    class Meta:
        model = CarBooking
        fields = ['pickup_location', 'drop_location', 'pickup_date', 'return_date',
                  'with_driver', 'total_amount', 'status', 'special_requests']
        widgets = {
            'pickup_location': forms.TextInput(attrs={'class': 'form-control'}),
            'drop_location': forms.TextInput(attrs={'class': 'form-control'}),
            'pickup_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'with_driver': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


from django.contrib.auth.models import User
from users.models import UserProfile


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    is_active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    is_staff = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_active', 'is_staff']


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'date_of_birth', 'address', 'city', 'state', 'country',
                  'passport_number', 'emergency_contact']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
        }
