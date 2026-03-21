from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap, TourSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'tours': TourSitemap,
}

urlpatterns = [
    path('', include('core.urls')),
    path('panel/', include('core.custom_admin_urls')),
    path('tours/', include('tours.urls')),
    path('bookings/', include('bookings.urls')),
    path('users/', include('users.urls')),
    path('vehicles/', include('vehicles.urls')),
    path('hotels/', include('hotels.urls')),
    path('blog/', include('blog.urls')),
    path('gallery/', include('gallery.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
