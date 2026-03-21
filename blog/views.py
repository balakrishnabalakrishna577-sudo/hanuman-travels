from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import BlogPost, BlogCategory


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    category_filter = request.GET.get('category', '')
    if category_filter:
        posts = posts.filter(category__slug=category_filter)
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    posts_page = paginator.get_page(page)
    categories = BlogCategory.objects.all()
    context = {
        'posts': posts_page,
        'categories': categories,
        'meta_title': 'Travel Blog - Hanuman Tours and Travels',
        'meta_description': 'Read our travel stories, tips and destination guides - Hanuman Tours and Travels.',
    }
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    post.views += 1
    post.save(update_fields=['views'])
    related = BlogPost.objects.filter(is_published=True, category=post.category).exclude(id=post.id)[:3]
    context = {
        'post': post,
        'related': related,
        'meta_title': f'{post.title} - Hanuman Tours and Travels Blog',
        'meta_description': post.excerpt,
    }
    return render(request, 'blog/blog_detail.html', context)
