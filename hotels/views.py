from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Hotel, HotelBooking
from .forms import HotelBookingForm
from core.models import Destination


def hotel_list(request):
    hotels = Hotel.objects.filter(is_active=True)
    destination_filter = request.GET.get('destination', '')
    stars_filter = request.GET.get('stars', '')
    if destination_filter:
        hotels = hotels.filter(destination__id=destination_filter)
    if stars_filter:
        hotels = hotels.filter(stars=stars_filter)
    destinations = Destination.objects.all()
    context = {
        'hotels': hotels,
        'destinations': destinations,
        'meta_title': 'Hotel Booking - Hanuman Tours and Travels',
        'meta_description': 'Book hotels across India at best prices with Hanuman Tours and Travels.',
    }
    return render(request, 'hotels/hotel_list.html', context)


def hotel_detail(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug, is_active=True)
    context = {'hotel': hotel, 'meta_title': f'{hotel.name} - Hanuman Tours and Travels'}
    return render(request, 'hotels/hotel_detail.html', context)


@login_required
def book_hotel(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug, is_active=True)
    form = HotelBookingForm(hotel=hotel)
    if request.method == 'POST':
        form = HotelBookingForm(request.POST, hotel=hotel)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.hotel = hotel
            nights = (booking.check_out - booking.check_in).days or 1
            booking.total_amount = booking.room_type.price_per_night * booking.num_rooms * nights
            booking.save()
            messages.success(request, f'Hotel booking confirmed! ID: {booking.booking_id}')
            return redirect('user_dashboard')
    context = {'hotel': hotel, 'form': form}
    return render(request, 'hotels/book_hotel.html', context)
