from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vehicle, CarBooking, AirportTransfer
from .forms import CarBookingForm, AirportTransferForm

# Pricing per vehicle type for airport transfer
TRANSFER_PRICING = {
    'sedan': 800,
    'suv': 1200,
    'tempo': 2000,
    'bus': 3500,
}


def vehicle_list(request):
    vehicles = Vehicle.objects.filter(is_available=True)
    vehicle_type = request.GET.get('type', '')
    if vehicle_type:
        vehicles = vehicles.filter(vehicle_type=vehicle_type)
    context = {
        'vehicles': vehicles,
        'vehicle_types': Vehicle.TYPE_CHOICES,
        'meta_title': 'Car Rental - Hanuman Tours and Travels',
        'meta_description': 'Rent a car or hire a vehicle for your travel needs with Hanuman Tours and Travels.',
    }
    return render(request, 'vehicles/vehicle_list.html', context)


@login_required
def book_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, is_available=True)
    form = CarBookingForm()
    if request.method == 'POST':
        form = CarBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.vehicle = vehicle
            days = (booking.return_date - booking.pickup_date).days or 1
            booking.total_amount = vehicle.price_per_day * days
            booking.save()
            messages.success(request, f'Car booking confirmed! ID: {booking.booking_id}')
            return redirect('user_dashboard')
    context = {'vehicle': vehicle, 'form': form}
    return render(request, 'vehicles/book_vehicle.html', context)


def airport_transfer(request):
    form = AirportTransferForm()
    pricing = TRANSFER_PRICING

    if request.method == 'POST':
        form = AirportTransferForm(request.POST)
        if form.is_valid():
            transfer = form.save(commit=False)
            if request.user.is_authenticated:
                transfer.user = request.user
            # Calculate price
            base = TRANSFER_PRICING.get(transfer.vehicle_type, 800)
            transfer.total_amount = base * 2 if transfer.transfer_type == 'both' else base
            transfer.save()
            messages.success(
                request,
                f'Airport transfer booked! Booking ID: {transfer.booking_id}. We will contact you shortly.'
            )
            return redirect('airport_transfer_success', booking_id=transfer.booking_id)

    context = {
        'form': form,
        'pricing': pricing,
        'meta_title': 'Airport Pickup & Drop - Hanuman Tours and Travels',
        'meta_description': 'Book airport pickup and drop service with Hanuman Tours and Travels. AC vehicles, professional drivers.',
    }
    return render(request, 'vehicles/airport_transfer.html', context)


def airport_transfer_success(request, booking_id):
    transfer = get_object_or_404(AirportTransfer, booking_id=booking_id)
    return render(request, 'vehicles/airport_transfer_success.html', {'transfer': transfer})
