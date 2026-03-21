from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from tours.models import TourPackage


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['home', 'about', 'contact', 'gallery_list', 'blog_list']

    def location(self, item):
        return reverse(item)


class TourSitemap(Sitemap):
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        return TourPackage.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('tour_detail', kwargs={'slug': obj.slug})
