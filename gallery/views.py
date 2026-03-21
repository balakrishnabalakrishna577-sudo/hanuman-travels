from django.shortcuts import render
from .models import GalleryImage, GalleryCategory


def gallery_list(request):
    categories = GalleryCategory.objects.all()
    category_filter = request.GET.get('category', '')
    images = GalleryImage.objects.all()
    if category_filter:
        images = images.filter(category__slug=category_filter)

    context = {
        'images': images,
        'categories': categories,
        'active_category': category_filter,
        'use_sample': not images.exists() and not category_filter,
        'meta_title': 'Gallery - Hanuman Tours And Travels',
        'meta_description': 'Explore our travel photo gallery - Hanuman Tours And Travels.',
    }
    return render(request, 'gallery/gallery.html', context)
