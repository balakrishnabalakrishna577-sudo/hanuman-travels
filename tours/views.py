from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import TourPackage, Review
from core.models import Destination
from .forms import ReviewForm


def tour_list(request):
    tours = TourPackage.objects.filter(is_active=True)
    destinations = Destination.objects.all().order_by('name')

    destination_filter = request.GET.get('destination', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    duration = request.GET.get('duration', '')
    tour_type = request.GET.get('type', '')
    sort = request.GET.get('sort', '')

    if destination_filter:
        tours = tours.filter(destination__id=destination_filter)
    if min_price:
        tours = tours.filter(price_per_person__gte=min_price)
    if max_price:
        tours = tours.filter(price_per_person__lte=max_price)
    if duration:
        tours = tours.filter(duration_days__lte=duration)
    if tour_type:
        tours = tours.filter(tour_type=tour_type)
    if sort == 'price_asc':
        tours = tours.order_by('price_per_person')
    elif sort == 'price_desc':
        tours = tours.order_by('-price_per_person')
    elif sort == 'duration':
        tours = tours.order_by('duration_days')

    paginator = Paginator(tours, 9)
    page = request.GET.get('page')
    tours_page = paginator.get_page(page)

    # Use the model's image_src property — it already has all local + Unsplash fallbacks
    destinations_with_images = [
        {'dest': d, 'img': d.image_src}
        for d in destinations
    ]

    context = {
        'tours': tours_page,
        'destinations': destinations,
        'destinations_with_images': destinations_with_images,
        'active_destination': destination_filter,
        'tour_types': TourPackage.TYPE_CHOICES,
        'meta_title': 'Tour Packages - Hanuman Tours and Travels',
        'meta_description': 'Explore our wide range of tour packages across India and abroad with Hanuman Tours and Travels.',
    }
    if request.user.is_authenticated:
        from core.models import Wishlist
        wishlist_tour_ids = Wishlist.objects.filter(user=request.user).values_list('tour_id', flat=True)
        context['user_wishlist'] = list(wishlist_tour_ids)
    else:
        context['user_wishlist'] = []
    return render(request, 'tours/tour_list.html', context)


def tour_detail(request, slug):
    tour = get_object_or_404(TourPackage, slug=slug, is_active=True)
    reviews = tour.reviews.filter(is_approved=True)
    related_tours = TourPackage.objects.filter(
        destination=tour.destination, is_active=True
    ).exclude(id=tour.id)[:3]

    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(tour=tour, user=request.user).first()

    review_form = ReviewForm()
    if request.method == 'POST' and request.user.is_authenticated:
        if user_review:
            messages.warning(request, 'You have already reviewed this tour.')
        else:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.tour = tour
                review.user = request.user
                review.save()
                messages.success(request, 'Your review has been submitted for approval.')
                return redirect('tour_detail', slug=slug)

    context = {
        'tour': tour,
        'reviews': reviews,
        'related_tours': related_tours,
        'review_form': review_form,
        'user_review': user_review,
        'meta_title': f'{tour.title} - Hanuman Tours and Travels',
        'meta_description': tour.description[:160],
    }
    return render(request, 'tours/tour_detail.html', context)
