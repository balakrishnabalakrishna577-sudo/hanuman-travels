from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from bookings.models import Booking
from vehicles.models import CarBooking
from hotels.models import HotelBooking
from .models import UserProfile
from .forms import RegisterForm, LoginForm, ProfileForm, UserUpdateForm


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Your account has been created.')
            return redirect('user_dashboard')
    return render(request, 'users/register.html', {'form': form, 'meta_title': 'Register - Hanuman Tours and Travels'})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                next_url = request.GET.get('next', '')
                # Never redirect site login to admin — admin has its own login
                if next_url and not next_url.startswith('/admin'):
                    return redirect(next_url)
                return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html', {'form': form, 'meta_title': 'Login - Hanuman Tours and Travels'})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard(request):
    from core.models import Wishlist
    from blog.models import BlogPost
    from vehicles.models import AirportTransfer
    from gallery.models import GalleryImage
    tour_bookings = Booking.objects.filter(user=request.user)[:5]
    car_bookings = CarBooking.objects.filter(user=request.user)[:5]
    airport_transfers = AirportTransfer.objects.filter(user=request.user).order_by('-created_at')[:5]
    wishlist_tours = Wishlist.objects.filter(user=request.user).select_related('tour', 'tour__destination')
    recent_blogs = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:3]
    gallery_images = GalleryImage.objects.select_related('category').order_by('-created_at')[:6]
    sample_gallery = [
        {'thumb': '/static/images/WebSites Images Travels/Gokarna.webp',       'full': '/static/images/WebSites Images Travels/Gokarna.webp',       'title': 'Gokarna Beach'},
        {'thumb': '/static/images/WebSites Images Travels/kanyakumari.webp',   'full': '/static/images/WebSites Images Travels/kanyakumari.webp',   'title': 'Kanyakumari'},
        {'thumb': '/static/images/WebSites Images Travels/Chikkamanglore.png', 'full': '/static/images/WebSites Images Travels/Chikkamanglore.png', 'title': 'Chikkamagaluru'},
        {'thumb': '/static/images/WebSites Images Travels/JogFals.jpeg',       'full': '/static/images/WebSites Images Travels/JogFals.jpeg',       'title': 'Jog Falls'},
        {'thumb': '/static/images/WebSites Images Travels/Rameswaram.webp',    'full': '/static/images/WebSites Images Travels/Rameswaram.webp',    'title': 'Rameswaram'},
        {'thumb': '/static/images/WebSites Images Travels/Madurai.jpg',        'full': '/static/images/WebSites Images Travels/Madurai.jpg',        'title': 'Madurai'},
    ]
    context = {
        'tour_bookings': tour_bookings,
        'car_bookings': car_bookings,
        'airport_transfers': airport_transfers,
        'wishlist_tours': wishlist_tours,
        'recent_blogs': recent_blogs,
        'gallery_images': gallery_images,
        'sample_gallery': sample_gallery,
        'meta_title': 'My Dashboard - Hanuman Tours and Travels',
    }
    return render(request, 'users/dashboard.html', context)


@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileForm(instance=profile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_dashboard')

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'meta_title': 'Edit Profile - Hanuman Tours and Travels',
    }
    return render(request, 'users/edit_profile.html', context)
