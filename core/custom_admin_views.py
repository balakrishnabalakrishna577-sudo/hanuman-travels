from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.contrib.auth.models import User
from django.utils import timezone

from core.models import Destination, ContactMessage, Newsletter, Testimonial, TeamMember
from tours.models import TourPackage, Review
from bookings.models import Booking
from vehicles.models import Vehicle, CarBooking, AirportTransfer
from blog.models import BlogPost, BlogCategory
from gallery.models import GalleryImage, GalleryCategory
from .custom_admin_forms import (
    TourForm, DestinationForm, VehicleForm,
    BlogPostForm, GalleryImageForm, TestimonialForm,
    TourBookingEditForm, CarBookingEditForm,
    UserEditForm, UserProfileEditForm,
)


def is_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

staff_required = user_passes_test(is_staff, login_url='/panel/login/')


# ── ADMIN LOGIN / LOGOUT ──────────────────────────────────────────────────────

def admin_login(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('custom_admin_dashboard')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and (user.is_staff or user.is_superuser):
            login(request, user)
            return redirect('custom_admin_dashboard')
        else:
            error = 'Invalid credentials or you do not have admin access.'
    return render(request, 'custom_admin/login.html', {'error': error})


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


def _sidebar_context():
    return {
        'pending_tour_bookings': Booking.objects.filter(status='pending').count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'pending_airport_transfers': AirportTransfer.objects.filter(status='pending').count(),
    }


@login_required
@staff_required
def dashboard(request):
    today = timezone.now().date()
    ctx = _sidebar_context()
    ctx.update({
        'total_tour_bookings': Booking.objects.count(),
        'pending_tour_bookings': Booking.objects.filter(status='pending').count(),
        'total_car_bookings': CarBooking.objects.count(),
        'pending_car_bookings': CarBooking.objects.filter(status='pending').count(),
        'total_airport_transfers': AirportTransfer.objects.count(),
        'pending_airport_transfers': AirportTransfer.objects.filter(status='pending').count(),
        'total_users': User.objects.count(),
        'new_users_today': User.objects.filter(date_joined__date=today).count(),
        'total_revenue': Booking.objects.filter(status__in=['confirmed', 'completed']).aggregate(t=Sum('total_amount'))['t'] or 0,
        'total_tours': TourPackage.objects.count(),
        'total_subscribers': Newsletter.objects.filter(is_active=True).count(),
        'recent_bookings': Booking.objects.select_related('user', 'tour').order_by('-created_at')[:8],
        'recent_messages': ContactMessage.objects.order_by('-created_at')[:6],
    })
    return render(request, 'custom_admin/dashboard.html', ctx)


# ── BOOKINGS ──────────────────────────────────────────────────────────────────

@login_required
@staff_required
def tour_bookings(request):
    qs = Booking.objects.select_related('user', 'tour').order_by('-created_at')
    status = request.GET.get('status')
    q = request.GET.get('q', '')
    if status:
        qs = qs.filter(status=status)
    if q:
        qs = qs.filter(Q(booking_id__icontains=q) | Q(user__username__icontains=q) | Q(tour__title__icontains=q))
    page = Paginator(qs, 20).get_page(request.GET.get('page'))
    ctx = _sidebar_context()
    ctx.update({'bookings': page, 'title': 'Tour Bookings', 'booking_type': 'tour'})
    return render(request, 'custom_admin/bookings.html', ctx)


@login_required
@staff_required
def car_bookings(request):
    qs = CarBooking.objects.select_related('user', 'vehicle').order_by('-created_at')
    status = request.GET.get('status')
    q = request.GET.get('q', '')
    if status:
        qs = qs.filter(status=status)
    if q:
        qs = qs.filter(Q(booking_id__icontains=q) | Q(user__username__icontains=q) | Q(vehicle__name__icontains=q))
    page = Paginator(qs, 20).get_page(request.GET.get('page'))
    ctx = _sidebar_context()
    ctx.update({'bookings': page, 'title': 'Car Bookings', 'booking_type': 'car'})
    return render(request, 'custom_admin/bookings.html', ctx)


@login_required
@staff_required
def booking_status(request, booking_type, pk):
    if request.method == 'POST':
        status = request.POST.get('status')
        if booking_type == 'tour':
            obj = get_object_or_404(Booking, pk=pk)
            redirect_url = 'custom_admin_tour_bookings'
        else:
            obj = get_object_or_404(CarBooking, pk=pk)
            redirect_url = 'custom_admin_car_bookings'
        obj.status = status
        obj.save()
        messages.success(request, f'Booking status updated to {status}.')
        return redirect(redirect_url)
    return redirect('custom_admin_dashboard')


@login_required
@staff_required
def booking_payment_status(request, pk):
    if request.method == 'POST':
        obj = get_object_or_404(Booking, pk=pk)
        obj.payment_status = request.POST.get('payment_status')
        obj.save()
        messages.success(request, f'Payment status updated.')
    return redirect('custom_admin_tour_bookings')


# ── TOURS ─────────────────────────────────────────────────────────────────────

@login_required
@staff_required
def tours_list(request):
    qs = TourPackage.objects.select_related('destination').order_by('-created_at')
    q = request.GET.get('q', '')
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(destination__name__icontains=q))
    page = Paginator(qs, 15).get_page(request.GET.get('page'))
    rows = []
    for t in page:
        rows.append({
            'cells': [
                t.title,
                t.destination.name,
                f'₹{t.final_price}',
                f'{t.duration_days}D/{t.duration_nights}N',
                '<span class="badge bg-success">Active</span>' if t.is_active else '<span class="badge bg-secondary">Inactive</span>',
                '<span class="badge bg-warning text-dark">Featured</span>' if t.is_featured else '',
            ],
            'edit_url': f'/panel/tours/{t.id}/edit/',
            'delete_url': f'/panel/tours/{t.id}/delete/',
        })
    ctx = _sidebar_context()
    ctx.update({
        'title': 'Tour Packages', 'columns': ['Title', 'Destination', 'Price', 'Duration', 'Status', 'Featured'],
        'rows': rows, 'page_obj': page, 'add_url': '/panel/tours/add/',
    })
    return render(request, 'custom_admin/list.html', ctx)


@login_required
@staff_required
def tour_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(TourPackage, pk=pk).delete()
        messages.success(request, 'Tour package deleted.')
    return redirect('custom_admin_tours')


# ── DESTINATIONS ──────────────────────────────────────────────────────────────

@login_required
@staff_required
def destinations_list(request):
    qs = Destination.objects.all()
    q = request.GET.get('q', '')
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(country__icontains=q))
    page = Paginator(qs, 15).get_page(request.GET.get('page'))
    rows = []
    for d in page:
        rows.append({
            'cells': [
                d.name, d.country, d.state or '-',
                '<span class="badge bg-success">Popular</span>' if d.is_popular else '<span class="badge bg-secondary">Normal</span>',
            ],
            'edit_url': f'/panel/destinations/{d.id}/edit/',
            'delete_url': f'/panel/destinations/{d.id}/delete/',
        })
    ctx = _sidebar_context()
    ctx.update({
        'title': 'Destinations', 'columns': ['Name', 'Country', 'State', 'Popular'],
        'rows': rows, 'page_obj': page, 'add_url': '/panel/destinations/add/',
    })
    return render(request, 'custom_admin/list.html', ctx)


@login_required
@staff_required
def destination_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Destination, pk=pk).delete()
        messages.success(request, 'Destination deleted.')
    return redirect('custom_admin_destinations')


# ── VEHICLES ──────────────────────────────────────────────────────────────────

@login_required
@staff_required
def vehicles_list(request):
    qs = Vehicle.objects.all()
    q = request.GET.get('q', '')
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(model__icontains=q))
    page = Paginator(qs, 15).get_page(request.GET.get('page'))
    rows = []
    for v in page:
        rows.append({
            'cells': [
                v.name, v.get_vehicle_type_display(), v.model,
                f'{v.capacity} seats', f'₹{v.price_per_day}/day',
                '<span class="badge bg-success">Available</span>' if v.is_available else '<span class="badge bg-danger">Unavailable</span>',
            ],
            'edit_url': f'/panel/vehicles/{v.id}/edit/',
            'delete_url': f'/panel/vehicles/{v.id}/delete/',
        })
    ctx = _sidebar_context()
    ctx.update({
        'title': 'Vehicles', 'columns': ['Name', 'Type', 'Model', 'Capacity', 'Price', 'Status'],
        'rows': rows, 'page_obj': page, 'add_url': '/panel/vehicles/add/',
    })
    return render(request, 'custom_admin/list.html', ctx)


@login_required
@staff_required
def vehicle_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Vehicle, pk=pk).delete()
        messages.success(request, 'Vehicle deleted.')
    return redirect('custom_admin_vehicles')


# ── BLOG ──────────────────────────────────────────────────────────────────────

@login_required
@staff_required
def blog_list(request):
    qs = BlogPost.objects.select_related('author', 'category').order_by('-created_at')
    q = request.GET.get('q', '')
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(author__username__icontains=q))
    page = Paginator(qs, 15).get_page(request.GET.get('page'))
    rows = []
    for b in page:
        rows.append({
            'cells': [
                b.title[:40], b.author.username,
                b.category.name if b.category else '-',
                str(b.views),
                '<span class="badge bg-success">Published</span>' if b.is_published else '<span class="badge bg-secondary">Draft</span>',
                b.created_at.strftime('%d %b %Y'),
            ],
            'edit_url': f'/panel/blog/{b.id}/edit/',
            'delete_url': f'/panel/blog/{b.id}/delete/',
        })
    ctx = _sidebar_context()
    ctx.update({
        'title': 'Blog Posts', 'columns': ['Title', 'Author', 'Category', 'Views', 'Status', 'Date'],
        'rows': rows, 'page_obj': page, 'add_url': '/panel/blog/add/',
    })
    return render(request, 'custom_admin/list.html', ctx)


@login_required
@staff_required
def blog_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(BlogPost, pk=pk).delete()
        messages.success(request, 'Blog post deleted.')
    return redirect('custom_admin_blog')


# ── GALLERY ───────────────────────────────────────────────────────────────────

@login_required
@staff_required
def gallery_list(request):
    qs = GalleryImage.objects.select_related('category').order_by('-created_at')
    page = Paginator(qs, 15).get_page(request.GET.get('page'))
    rows = []
    for g in page:
        rows.append({
            'cells': [
                g.title, g.category.name,
                '<span class="badge bg-warning text-dark">Featured</span>' if g.is_featured else '-',
                g.created_at.strftime('%d %b %Y'),
            ],
            'edit_url': f'/panel/gallery/{g.id}/edit/',
            'delete_url': f'/panel/gallery/{g.id}/delete/',
        })
    ctx = _sidebar_context()
    ctx.update({
        'title': 'Gallery', 'columns': ['Title', 'Category', 'Featured', 'Date'],
        'rows': rows, 'page_obj': page, 'add_url': '/panel/gallery/add/',
    })
    return render(request, 'custom_admin/list.html', ctx)


@login_required
@staff_required
def gallery_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(GalleryImage, pk=pk).delete()
        messages.success(request, 'Image deleted.')
    return redirect('custom_admin_gallery')


# ── USERS ─────────────────────────────────────────────────────────────────────

@login_required
@staff_required
def users_list(request):
    qs = User.objects.order_by('-date_joined')
    q = request.GET.get('q', '')
    if q:
        qs = qs.filter(Q(username__icontains=q) | Q(email__icontains=q) | Q(first_name__icontains=q))
    page = Paginator(qs, 20).get_page(request.GET.get('page'))
    rows = []
    for u in page:
        rows.append({
            'cells': [
                u.get_full_name() or u.username, u.email,
                u.date_joined.strftime('%d %b %Y'),
                '<span class="badge bg-warning text-dark">Staff</span>' if u.is_staff else '<span class="badge bg-secondary">User</span>',
                '<span class="badge bg-success">Active</span>' if u.is_active else '<span class="badge bg-danger">Inactive</span>',
            ],
            'edit_url': f'/panel/users/{u.id}/edit/',
            'delete_url': None,
        })
    ctx = _sidebar_context()
    ctx.update({
        'title': 'Users', 'columns': ['Name', 'Email', 'Joined', 'Role', 'Status'],
        'rows': rows, 'page_obj': page,
    })
    return render(request, 'custom_admin/list.html', ctx)


# ── MESSAGES ──────────────────────────────────────────────────────────────────

@login_required
@staff_required
def contact_messages(request):
    qs = ContactMessage.objects.order_by('-created_at')
    status = request.GET.get('status')
    if status == 'unread':
        qs = qs.filter(is_read=False)
    elif status == 'read':
        qs = qs.filter(is_read=True)
    ctx = _sidebar_context()
    ctx.update({'messages_list': qs})
    return render(request, 'custom_admin/messages.html', ctx)


@login_required
@staff_required
def mark_message_read(request, pk):
    if request.method == 'POST':
        msg = get_object_or_404(ContactMessage, pk=pk)
        msg.is_read = True
        msg.save()
        messages.success(request, 'Message marked as read.')
    return redirect('custom_admin_messages')


@login_required
@staff_required
def delete_message(request, pk):
    if request.method == 'POST':
        get_object_or_404(ContactMessage, pk=pk).delete()
        messages.success(request, 'Message deleted.')
    return redirect('custom_admin_messages')


# ── NEWSLETTER ────────────────────────────────────────────────────────────────

@login_required
@staff_required
def newsletter_list(request):
    qs = Newsletter.objects.order_by('-subscribed_at')
    page = Paginator(qs, 20).get_page(request.GET.get('page'))
    rows = []
    for n in page:
        rows.append({
            'cells': [
                n.email,
                n.subscribed_at.strftime('%d %b %Y'),
                '<span class="badge bg-success">Active</span>' if n.is_active else '<span class="badge bg-secondary">Inactive</span>',
            ],
            'edit_url': None,
            'delete_url': f'/panel/newsletter/{n.id}/delete/',
        })
    ctx = _sidebar_context()
    ctx.update({
        'title': 'Newsletter Subscribers', 'columns': ['Email', 'Subscribed', 'Status'],
        'rows': rows, 'page_obj': page,
    })
    return render(request, 'custom_admin/list.html', ctx)


@login_required
@staff_required
def newsletter_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Newsletter, pk=pk).delete()
        messages.success(request, 'Subscriber removed.')
    return redirect('custom_admin_newsletter')


# ── TESTIMONIALS ──────────────────────────────────────────────────────────────

@login_required
@staff_required
def testimonials_list(request):
    qs = Testimonial.objects.order_by('-created_at')
    page = Paginator(qs, 15).get_page(request.GET.get('page'))
    rows = []
    for t in page:
        rows.append({
            'cells': [
                t.name, t.location or '-',
                '⭐' * t.rating,
                t.message[:60] + '...' if len(t.message) > 60 else t.message,
                '<span class="badge bg-success">Active</span>' if t.is_active else '<span class="badge bg-secondary">Hidden</span>',
            ],
            'edit_url': f'/panel/testimonials/{t.id}/edit/',
            'delete_url': f'/panel/testimonials/{t.id}/delete/',
        })
    ctx = _sidebar_context()
    ctx.update({
        'title': 'Testimonials', 'columns': ['Name', 'Location', 'Rating', 'Message', 'Status'],
        'rows': rows, 'page_obj': page, 'add_url': '/panel/testimonials/add/',
    })
    return render(request, 'custom_admin/list.html', ctx)


@login_required
@staff_required
def testimonial_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Testimonial, pk=pk).delete()
        messages.success(request, 'Testimonial deleted.')
    return redirect('custom_admin_testimonials')


# ── TOUR ADD / EDIT ───────────────────────────────────────────────────────────

@login_required
@staff_required
def tour_add(request):
    form = TourForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Tour package added successfully.')
        return redirect('custom_admin_tours')
    ctx = _sidebar_context()
    ctx.update({'form': form, 'title': 'Add Tour Package', 'back_url': '/panel/tours/'})
    return render(request, 'custom_admin/form.html', ctx)


@login_required
@staff_required
def tour_edit(request, pk):
    obj = get_object_or_404(TourPackage, pk=pk)
    form = TourForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Tour package updated.')
        return redirect('custom_admin_tours')
    ctx = _sidebar_context()
    ctx.update({'form': form, 'title': f'Edit: {obj.title}', 'back_url': '/panel/tours/'})
    return render(request, 'custom_admin/form.html', ctx)


# ── DESTINATION ADD / EDIT ────────────────────────────────────────────────────

@login_required
@staff_required
def destination_add(request):
    form = DestinationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Destination added.')
        return redirect('custom_admin_destinations')
    ctx = _sidebar_context()
    ctx.update({'form': form, 'title': 'Add Destination', 'back_url': '/panel/destinations/'})
    return render(request, 'custom_admin/form.html', ctx)


@login_required
@staff_required
def destination_edit(request, pk):
    obj = get_object_or_404(Destination, pk=pk)
    form = DestinationForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Destination updated.')
        return redirect('custom_admin_destinations')
    ctx = _sidebar_context()
    ctx.update({'form': form, 'title': f'Edit: {obj.name}', 'back_url': '/panel/destinations/'})
    return render(request, 'custom_admin/form.html', ctx)


# ── VEHICLE ADD / EDIT ────────────────────────────────────────────────────────

@login_required
@staff_required
def vehicle_add(request):
    form = VehicleForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Vehicle added.')
        return redirect('custom_admin_vehicles')
    ctx = _sidebar_context()
    ctx.update({'form': form, 'title': 'Add Vehicle', 'back_url': '/panel/vehicles/'})
    return render(request, 'custom_admin/form.html', ctx)


@login_required
@staff_required
def vehicle_edit(request, pk):
    obj = get_object_or_404(Vehicle, pk=pk)
    form = VehicleForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Vehicle updated.')
        return redirect('custom_admin_vehicles')
    ctx = _sidebar_context()
    ctx.update({'form': form, 'title': f'Edit: {obj.name}', 'back_url': '/panel/vehicles/'})
    return render(request, 'custom_admin/form.html', ctx)


# ── BLOG ADD / EDIT ───────────────────────────────────────────────────────────

@login_required
@staff_required
def blog_add(request):
    form = BlogPostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Blog post added.')
        return redirect('custom_admin_blog')
    ctx = _sidebar_context()
    ctx.update({'form': form, 'title': 'Add Blog Post', 'back_url': '/panel/blog/'})
    return render(request, 'custom_admin/form.html', ctx)


@login_required
@staff_required
def blog_edit(request, pk):
    obj = get_object_or_404(BlogPost, pk=pk)
    form = BlogPostForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Blog post updated.')
        return redirect('custom_admin_blog')
    ctx = _sidebar_context()
    ctx.update({'form': form, 'title': f'Edit: {obj.title[:40]}', 'back_url': '/panel/blog/'})
    return render(request, 'custom_admin/form.html', ctx)


# ── GALLERY ADD / EDIT ────────────────────────────────────────────────────────

@login_required
@staff_required
def gallery_add(request):
    form = GalleryImageForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Gallery image added.')
        return redirect('custom_admin_gallery')
    ctx = _sidebar_context()
    ctx.update({'form': form, 'title': 'Add Gallery Image', 'back_url': '/panel/gallery/'})
    return render(request, 'custom_admin/form.html', ctx)


@login_required
@staff_required
def gallery_edit(request, pk):
    obj = get_object_or_404(GalleryImage, pk=pk)
    form = GalleryImageForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Gallery image updated.')
        return redirect('custom_admin_gallery')
    ctx = _sidebar_context()
    ctx.update({'form': form, 'title': f'Edit: {obj.title}', 'back_url': '/panel/gallery/'})
    return render(request, 'custom_admin/form.html', ctx)


# ── TESTIMONIAL ADD / EDIT ────────────────────────────────────────────────────

@login_required
@staff_required
def testimonial_add(request):
    form = TestimonialForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Testimonial added.')
        return redirect('custom_admin_testimonials')
    ctx = _sidebar_context()
    ctx.update({'form': form, 'title': 'Add Testimonial', 'back_url': '/panel/testimonials/'})
    return render(request, 'custom_admin/form.html', ctx)


@login_required
@staff_required
def testimonial_edit(request, pk):
    obj = get_object_or_404(Testimonial, pk=pk)
    form = TestimonialForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Testimonial updated.')
        return redirect('custom_admin_testimonials')
    ctx = _sidebar_context()
    ctx.update({'form': form, 'title': f'Edit: {obj.name}', 'back_url': '/panel/testimonials/'})
    return render(request, 'custom_admin/form.html', ctx)


# ── BOOKING EDIT VIEWS ────────────────────────────────────────────────────────

@login_required
@staff_required
def tour_booking_edit(request, pk):
    obj = get_object_or_404(Booking, pk=pk)
    form = TourBookingEditForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Booking {obj.booking_id} updated.')
        return redirect('custom_admin_tour_bookings')
    ctx = _sidebar_context()
    ctx.update({
        'form': form,
        'title': f'Edit Tour Booking — {obj.booking_id}',
        'back_url': '/panel/bookings/tours/',
        'booking': obj,
    })
    return render(request, 'custom_admin/booking_edit.html', ctx)


@login_required
@staff_required
def car_booking_edit(request, pk):
    obj = get_object_or_404(CarBooking, pk=pk)
    form = CarBookingEditForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Booking {obj.booking_id} updated.')
        return redirect('custom_admin_car_bookings')
    ctx = _sidebar_context()
    ctx.update({
        'form': form,
        'title': f'Edit Car Booking — {obj.booking_id}',
        'back_url': '/panel/bookings/cars/',
        'booking': obj,
    })
    return render(request, 'custom_admin/booking_edit.html', ctx)


# ── USER EDIT ─────────────────────────────────────────────────────────────────

@login_required
@staff_required
def user_edit(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    # Get or create profile
    profile, _ = user_obj.profile.__class__.objects.get_or_create(user=user_obj) if hasattr(user_obj, 'profile') else (None, False)
    try:
        from users.models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=user_obj)
    except Exception:
        profile = None

    user_form = UserEditForm(request.POST or None, instance=user_obj)
    profile_form = UserProfileEditForm(request.POST or None, instance=profile) if profile else None

    if request.method == 'POST':
        u_valid = user_form.is_valid()
        p_valid = profile_form.is_valid() if profile_form else True
        if u_valid and p_valid:
            user_form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, f'User {user_obj.username} updated.')
            return redirect('custom_admin_users')

    ctx = _sidebar_context()
    ctx.update({
        'user_obj': user_obj,
        'user_form': user_form,
        'profile_form': profile_form,
        'title': f'Edit User — {user_obj.username}',
        'back_url': '/panel/users/',
    })
    return render(request, 'custom_admin/user_edit.html', ctx)


# ── AIRPORT TRANSFERS ─────────────────────────────────────────────────────────

@login_required
@staff_required
def airport_transfers(request):
    qs = AirportTransfer.objects.order_by('-created_at')
    status = request.GET.get('status')
    if status:
        qs = qs.filter(status=status)
    page = Paginator(qs, 15).get_page(request.GET.get('page'))
    ctx = _sidebar_context()
    ctx.update({'transfers': page, 'status_filter': status})
    return render(request, 'custom_admin/airport_transfers.html', ctx)


@login_required
@staff_required
def airport_transfer_status(request, pk):
    if request.method == 'POST':
        obj = get_object_or_404(AirportTransfer, pk=pk)
        obj.status = request.POST.get('status', obj.status)
        obj.payment_status = request.POST.get('payment_status', obj.payment_status)
        obj.save()
        messages.success(request, 'Transfer status updated.')
    return redirect('admin_airport_transfers')


# ── REVIEWS ───────────────────────────────────────────────────────────────────

@login_required
@staff_required
def reviews_list(request):
    status = request.GET.get('status', '')
    q = request.GET.get('q', '')
    qs = Review.objects.select_related('user', 'tour').order_by('-created_at')
    if status == 'approved':
        qs = qs.filter(is_approved=True)
    elif status == 'pending':
        qs = qs.filter(is_approved=False)
    if q:
        qs = qs.filter(Q(tour__title__icontains=q) | Q(user__username__icontains=q) | Q(title__icontains=q))
    page = Paginator(qs, 20).get_page(request.GET.get('page'))
    ctx = _sidebar_context()
    ctx.update({
        'reviews': page,
        'status_filter': status,
        'q': q,
        'pending_count': Review.objects.filter(is_approved=False).count(),
    })
    return render(request, 'custom_admin/reviews.html', ctx)


@login_required
@staff_required
def review_approve(request, pk):
    if request.method == 'POST':
        obj = get_object_or_404(Review, pk=pk)
        obj.is_approved = not obj.is_approved
        obj.save()
        state = 'approved' if obj.is_approved else 'hidden'
        messages.success(request, f'Review {state}.')
    return redirect('custom_admin_reviews')


@login_required
@staff_required
def review_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Review, pk=pk).delete()
        messages.success(request, 'Review deleted.')
    return redirect('custom_admin_reviews')
