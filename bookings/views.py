from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from tours.models import TourPackage
from .models import Booking
from .forms import BookingForm


@login_required
def create_booking(request, tour_slug):
    tour = get_object_or_404(TourPackage, slug=tour_slug, is_active=True)
    form = BookingForm()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.tour = tour
            num_people = booking.num_adults + booking.num_children
            booking.total_amount = tour.final_price * num_people
            booking.save()

            try:
                send_mail(
                    f'Booking Confirmed - {booking.booking_id}',
                    f'Dear {request.user.first_name},\n\nYour booking for {tour.title} has been received.\nBooking ID: {booking.booking_id}\nTravel Date: {booking.travel_date}\nTotal Amount: ₹{booking.total_amount}\n\nThank you for choosing Hanuman Tours!',
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(request, f'Booking confirmed! Your booking ID is {booking.booking_id}')
            return redirect('booking_detail', booking_id=booking.booking_id)

    context = {
        'tour': tour,
        'form': form,
        'meta_title': f'Book {tour.title} - Hanuman Tours and Travels',
    }
    return render(request, 'bookings/create_booking.html', context)


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    context = {'booking': booking}
    return render(request, 'bookings/booking_detail.html', context)


@login_required
def booking_print(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    return render(request, 'bookings/booking_print.html', {'booking': booking})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Your booking has been cancelled.')
    else:
        messages.error(request, 'This booking cannot be cancelled.')
    return redirect('user_dashboard')
