from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from tours.models import TourPackage, Review
from core.models import Destination, Testimonial, TeamMember, ContactMessage, Newsletter, Wishlist, FAQ
from blog.models import BlogPost
from gallery.models import GalleryImage
from .forms import ContactForm, NewsletterForm


def home(request):
    featured_tours = TourPackage.objects.filter(is_featured=True, is_active=True)[:6]
    popular_destinations = Destination.objects.filter(is_popular=True)[:8]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    recent_blogs = BlogPost.objects.filter(is_published=True)[:3]
    gallery_images = GalleryImage.objects.filter(is_featured=True)[:8]
    from vehicles.models import Vehicle
    featured_vehicles = Vehicle.objects.filter(is_available=True)[:4]
    newsletter_form = NewsletterForm()

    if request.method == 'POST' and 'newsletter' in request.POST:
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            messages.success(request, 'Thank you for subscribing to our newsletter!')
            return redirect('home')

    sample_tours = [
        {
            'title': 'Golden Triangle Tour',
            'destination': 'Delhi - Agra - Jaipur',
            'tour_type': 'Cultural',
            'duration': '6D/5N',
            'max_group': 20,
            'price': '12,999',
            'rating': 5,
            'reviews': 128,
            'image': 'https://images.unsplash.com/photo-1548013146-72479768bada?w=600&q=80',
            'badge': 'Best Seller',
            'badge_color': 'bg-danger',
        },
        {
            'title': 'Kerala Backwaters Escape',
            'destination': 'Kochi - Alleppey - Munnar',
            'tour_type': 'Nature',
            'duration': '5D/4N',
            'max_group': 15,
            'price': '10,499',
            'rating': 5,
            'reviews': 94,
            'image': 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=600&q=80',
            'badge': 'Popular',
            'badge_color': 'bg-warning text-dark',
        },
        {
            'title': 'Manali Snow Adventure',
            'destination': 'Manali - Solang - Rohtang',
            'tour_type': 'Adventure',
            'duration': '7D/6N',
            'max_group': 12,
            'price': '14,999',
            'rating': 4,
            'reviews': 76,
            'image': 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600&q=80',
            'badge': 'Adventure',
            'badge_color': 'bg-info',
        },
        {
            'title': 'Goa Beach Holiday',
            'destination': 'North Goa - South Goa',
            'tour_type': 'Beach',
            'duration': '4D/3N',
            'max_group': 25,
            'price': '8,999',
            'rating': 4,
            'reviews': 112,
            'image': 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&q=80',
            'badge': 'Budget',
            'badge_color': 'bg-success',
        },
        {
            'title': 'Rajasthan Royal Tour',
            'destination': 'Jaipur - Jodhpur - Udaipur',
            'tour_type': 'Cultural',
            'duration': '8D/7N',
            'max_group': 18,
            'price': '18,499',
            'rating': 5,
            'reviews': 89,
            'image': 'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=600&q=80',
            'badge': 'Premium',
            'badge_color': 'bg-warning text-dark',
        },
        {
            'title': 'Andaman Island Getaway',
            'destination': 'Port Blair - Havelock - Neil',
            'tour_type': 'Beach',
            'duration': '6D/5N',
            'max_group': 16,
            'price': '22,999',
            'rating': 5,
            'reviews': 67,
            'image': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80',
            'badge': 'Exotic',
            'badge_color': 'bg-primary',
        },
    ]

    # Map destination names to fallback images (local static files first)
    dest_image_map = {
        'baba budangiri':     '/static/images/WebSites Images Travels/Baba Budangiri.jpg',
        'belur':              '/static/images/WebSites Images Travels/Beluru.jpg',
        'chikkamagaluru':     '/static/images/WebSites Images Travels/Chikkamanglore.png',
        'eramala':            '/static/images/WebSites Images Travels/Eramale.jpg',
        'gokarna':            '/static/images/WebSites Images Travels/Gokarna.webp',
        'guruvayur':          '/static/images/WebSites Images Travels/Guruwire.webp',
        'halebidu':           '/static/images/WebSites Images Travels/Halebedu.webp',
        'honnavar':           '/static/images/WebSites Images Travels/Honnavara.jpg',
        'horanadu':           '/static/images/WebSites Images Travels/Horanadu.webp',
        'jatayu':             '/static/images/WebSites Images Travels/Jatayu Park.avif',
        'jog':                '/static/images/WebSites Images Travels/JogFals.jpeg',
        'kanyakumari':        '/static/images/WebSites Images Travels/kanyakumari.webp',
        'kolambiya':          '/static/images/WebSites Images Travels/Kolambiya Beach.jpg',
        'kudremukh':          '/static/images/WebSites Images Travels/Kudure Mukha.avif',
        'kukke':              '/static/images/WebSites Images Travels/Kuke.webp',
        'madurai':            '/static/images/WebSites Images Travels/Madurai.jpg',
        'malpe':              '/static/images/WebSites Images Travels/Malphe Beach.JPG',
        'maruvantha':         '/static/images/WebSites Images Travels/Maruvantha Beach.jpg',
        'mullayanagiri':      '/static/images/WebSites Images Travels/Mullaingiri Betta.jpg',
        'om beach':           '/static/images/WebSites Images Travels/Om Beach.jpg',
        'palani':             '/static/images/WebSites Images Travels/Palni.jpg',
        'palni':              '/static/images/WebSites Images Travels/Palni.jpg',
        'pampa':              '/static/images/WebSites Images Travels/Pampa.jpg',
        'rameswaram':         '/static/images/WebSites Images Travels/Rameswaram.webp',
        'sabarimala':         '/static/images/WebSites Images Travels/Sabarimale.avif',
        'sakleshpur':         '/static/images/WebSites Images Travels/Sakaleswara.jpg',
        'sigandur':           '/static/images/WebSites Images Travels/Sigandhur.jpg',
        'thiruvananthapuram': '/static/images/WebSites Images Travels/Trivenrum.jpg',
        'trivandrum':         '/static/images/WebSites Images Travels/Trivenrum.jpg',
        'udupi':              '/static/images/WebSites Images Travels/Udupi.jpg',
        'goa':                'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&q=80',
        'kerala':             'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=600&q=80',
        'rajasthan':          'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=600&q=80',
        'manali':             'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600&q=80',
        'himachal':           'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600&q=80',
        'andaman':            'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80',
        'varanasi':           'https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=600&q=80',
        'shimla':             'https://images.unsplash.com/photo-1597074866923-dc0589150358?w=600&q=80',
        'ooty':               'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&q=80',
        'kashmir':            'https://images.unsplash.com/photo-1566837945700-30057527ade0?w=600&q=80',
        'ladakh':             'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80',
        'agra':               'https://images.unsplash.com/photo-1548013146-72479768bada?w=600&q=80',
        'wayanad':            'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=600&q=80',
        'murudeshwar':        'https://images.unsplash.com/photo-1621996659490-3275b4d0d951?w=600&q=80',
    }
    default_fallback = 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&q=80'

    def get_dest_image(name):
        lower = name.lower()
        for key, url in dest_image_map.items():
            if key in lower:
                return url
        return default_fallback

    destinations_with_images = [
        {'dest': d, 'fallback': d.image_src}
        for d in popular_destinations
    ]
    sample_destinations = [
        {
            'name': 'Gokarna',
            'country': 'India', 'packages': 8,
            'image': '/static/images/WebSites Images Travels/Gokarna.webp',
        },
        {
            'name': 'Kanyakumari',
            'country': 'India', 'packages': 6,
            'image': '/static/images/WebSites Images Travels/kanyakumari.webp',
        },
        {
            'name': 'Chikkamagaluru',
            'country': 'India', 'packages': 10,
            'image': '/static/images/WebSites Images Travels/Chikkamanglore.png',
        },
        {
            'name': 'Jog Falls',
            'country': 'India', 'packages': 5,
            'image': '/static/images/WebSites Images Travels/JogFals.jpeg',
        },
        {
            'name': 'Rameswaram',
            'country': 'India', 'packages': 7,
            'image': '/static/images/WebSites Images Travels/Rameswaram.webp',
        },
        {
            'name': 'Madurai',
            'country': 'India', 'packages': 9,
            'image': '/static/images/WebSites Images Travels/Madurai.jpg',
        },
        {
            'name': 'Udupi',
            'country': 'India', 'packages': 6,
            'image': '/static/images/WebSites Images Travels/Udupi.jpg',
        },
        {
            'name': 'Kukke Subramanya',
            'country': 'India', 'packages': 4,
            'image': '/static/images/WebSites Images Travels/Kuke.webp',
        },
    ]

    context = {
        'featured_tours': featured_tours,
        'sample_tours': sample_tours,
        'popular_destinations': popular_destinations,
        'destinations_with_images': destinations_with_images,
        'sample_destinations': sample_destinations,
        'testimonials': testimonials,
        'recent_blogs': recent_blogs,
        'gallery_images': gallery_images,
        'featured_vehicles': featured_vehicles,
        'newsletter_form': newsletter_form,
        'sample_gallery_local': [
            {'src': '/static/images/WebSites Images Travels/Gokarna.webp',       'title': 'Gokarna'},
            {'src': '/static/images/WebSites Images Travels/kanyakumari.webp',   'title': 'Kanyakumari'},
            {'src': '/static/images/WebSites Images Travels/Chikkamanglore.png', 'title': 'Chikkamagaluru'},
            {'src': '/static/images/WebSites Images Travels/JogFals.jpeg',       'title': 'Jog Falls'},
            {'src': '/static/images/WebSites Images Travels/Rameswaram.webp',    'title': 'Rameswaram'},
            {'src': '/static/images/WebSites Images Travels/Madurai.jpg',        'title': 'Madurai'},
            {'src': '/static/images/WebSites Images Travels/Udupi.jpg',          'title': 'Udupi'},
            {'src': '/static/images/WebSites Images Travels/Om Beach.jpg',       'title': 'Om Beach'},
        ],
        'meta_title': 'Hanuman Tours and Travels - Your Journey, Our Responsibility',
        'meta_description': 'Explore India and beyond with Hanuman Tours and Travels. Best tour packages, car rentals, and hotel bookings.',
    }
    return render(request, 'core/home.html', context)


def about(request):
    team = TeamMember.objects.all()
    service_list = [
        {'icon': 'bi-compass-fill',    'title': 'Tour Packages',      'desc': 'Customized domestic and international tour packages for all budgets.'},
        {'icon': 'bi-car-front-fill',  'title': 'Car Rental',         'desc': 'Wide range of vehicles with experienced drivers for all your travel needs.'},
        {'icon': 'bi-building-fill',   'title': 'Hotel Booking',      'desc': 'Best hotels at competitive prices across all major destinations.'},
        {'icon': 'bi-airplane-fill',   'title': 'Flight Booking',     'desc': 'Domestic and international flight bookings at the best fares.'},
        {'icon': 'bi-heart-fill',      'title': 'Honeymoon Packages', 'desc': 'Romantic getaways crafted for couples to celebrate their love.'},
        {'icon': 'bi-people-fill',     'title': 'Group Tours',        'desc': 'Special group packages for corporate, school, and family trips.'},
    ]
    context = {
        'team': team,
        'service_list': service_list,
        'meta_title': 'About Us - Hanuman Tours and Travels',
        'meta_description': 'Learn about Hanuman Tours and Travels - our story, mission, vision and team.',
    }
    return render(request, 'core/about.html', context)


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()
            try:
                send_mail(
                    f"New Contact: {contact_msg.subject}",
                    f"From: {contact_msg.name}\nEmail: {contact_msg.email}\nPhone: {contact_msg.phone}\n\n{contact_msg.message}",
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.SITE_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, 'Your message has been sent! We will contact you soon.')
            return redirect('contact')
    context = {
        'form': form,
        'meta_title': 'Contact Us - Hanuman Tours and Travels',
        'meta_description': 'Get in touch with Hanuman Tours and Travels for bookings and inquiries.',
    }
    return render(request, 'core/contact.html', context)


def search_suggestions(request):
    from django.http import JsonResponse
    q = request.GET.get('q', '').strip()
    results = []
    if len(q) >= 2:
        from django.db.models import Q
        tours = TourPackage.objects.filter(
            is_active=True
        ).filter(
            Q(title__icontains=q) | Q(destination__name__icontains=q)
        ).select_related('destination')[:8]
        for t in tours:
            results.append({
                'label': t.title,
                'sub': t.destination.name,
                'type': 'tour',
                'url': f'/tours/{t.slug}/',
            })
        dests = Destination.objects.filter(name__icontains=q)[:4]
        for d in dests:
            results.append({
                'label': d.name,
                'sub': d.country,
                'type': 'destination',
                'url': f'/search/?q={d.name}',
            })
    return JsonResponse({'results': results})


def search(request):
    query = request.GET.get('q', '').strip()
    destination = request.GET.get('destination', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    duration = request.GET.get('duration', '')

    tours = TourPackage.objects.filter(is_active=True).select_related('destination')

    if query:
        from django.db.models import Q
        tours = tours.filter(
            Q(title__icontains=query) |
            Q(destination__name__icontains=query) |
            Q(description__icontains=query) |
            Q(tour_type__icontains=query)
        )
    if destination:
        tours = tours.filter(destination__id=destination)
    if min_price:
        try:
            tours = tours.filter(price_per_person__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            tours = tours.filter(price_per_person__lte=float(max_price))
        except ValueError:
            pass
    if duration:
        try:
            tours = tours.filter(duration_days__lte=int(duration))
        except ValueError:
            pass

    destinations = Destination.objects.all().order_by('name')
    context = {
        'tours': tours.distinct(),
        'query': query,
        'destination': destination,
        'min_price': min_price,
        'max_price': max_price,
        'duration': duration,
        'destinations': destinations,
        'meta_title': f'Search Results for "{query}" - Hanuman Tours and Travels',
    }
    return render(request, 'core/search.html', context)


def privacy_policy(request):
    return render(request, 'core/privacy_policy.html', {
        'meta_title': 'Privacy Policy - Hanuman Tours and Travels',
    })


def terms_of_service(request):
    return render(request, 'core/terms_of_service.html', {
        'meta_title': 'Terms of Service - Hanuman Tours and Travels',
    })


def faq(request):
    faqs = FAQ.objects.filter(is_active=True)
    categories = faqs.values_list('category', flat=True).distinct()
    context = {
        'faqs': faqs,
        'categories': categories,
        'meta_title': 'FAQ - Hanuman Tours and Travels',
        'meta_description': 'Frequently asked questions about Hanuman Tours and Travels.',
    }
    return render(request, 'core/faq.html', context)


@csrf_exempt
def wishlist_toggle(request, tour_id):
    from django.http import JsonResponse
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'login_required'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)
    tour = get_object_or_404(TourPackage, id=tour_id)
    obj, created = Wishlist.objects.get_or_create(user=request.user, tour=tour)
    if not created:
        obj.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'added'})
