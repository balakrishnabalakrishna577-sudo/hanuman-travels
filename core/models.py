from django.db import models
from django.contrib.auth.models import User


class Destination(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/', blank=True)
    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Keyword → image map (local static files take priority, Unsplash as final fallback)
    _FALLBACK_MAP = {
        'baba budangiri':     '/static/images/WebSites Images Travels/Baba Budangiri.jpg',
        'belur':              '/static/images/WebSites Images Travels/Beluru.jpg',
        'chikkamagaluru':     '/static/images/WebSites Images Travels/Chikkamanglore.png',
        'eramala':            '/static/images/WebSites Images Travels/Eramale.jpg',
        'gokarna':            '/static/images/WebSites Images Travels/Gokarna.webp',
        'guruvayur':          '/static/images/WebSites Images Travels/Guruwire.webp',
        'halebidu':           '/static/images/WebSites Images Travels/Halebedu.webp',
        'hajmala':            '/static/images/WebSites Images Travels/Horanadu.webp',
        'honnavar':           '/static/images/WebSites Images Travels/Honnavara.jpg',
        'horanadu':           '/static/images/WebSites Images Travels/Horanadu.webp',
        'jatayu':             '/static/images/WebSites Images Travels/Jatayu Park.avif',
        'jog':                '/static/images/WebSites Images Travels/JogFals.jpeg',
        'kanyakumari':        '/static/images/WebSites Images Travels/kanyakumari.webp',
        'kolambiya':          '/static/images/WebSites Images Travels/Kolambiya Beach.jpg',
        'kudremukh':          '/static/images/WebSites Images Travels/Kudure Mukha.avif',
        'kudure':             '/static/images/WebSites Images Travels/Kudure Mukha.avif',
        'kukke':              '/static/images/WebSites Images Travels/Kuke.webp',
        'madurai':            '/static/images/WebSites Images Travels/Madurai.jpg',
        'malpe':              '/static/images/WebSites Images Travels/Malphe Beach.JPG',
        'maruvantha':         '/static/images/WebSites Images Travels/Maruvantha Beach.jpg',
        'mullayanagiri':      '/static/images/WebSites Images Travels/Mullaingiri Betta.jpg',
        'mullaingiri':        '/static/images/WebSites Images Travels/Mullaingiri Betta.jpg',
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
        # Unsplash fallbacks for destinations without local images
        'goa':                'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&q=80',
        'kerala':             'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=600&q=80',
        'rajasthan':          '/static/images/WebSites Images Travels/Rajasthan.webp',
        'jaipur':             '/static/images/WebSites Images Travels/Rajasthan.webp',
        'jodhpur':            '/static/images/WebSites Images Travels/Rajasthan.webp',
        'udaipur':            '/static/images/WebSites Images Travels/Rajasthan.webp',
        'manali':             'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600&q=80',
        'himachal':           'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600&q=80',
        'shimla':             'https://images.unsplash.com/photo-1597074866923-dc0589150358?w=600&q=80',
        'andaman':            'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80',
        'varanasi':           'https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=600&q=80',
        'agra':               'https://images.unsplash.com/photo-1548013146-72479768bada?w=600&q=80',
        'taj mahal':          'https://images.unsplash.com/photo-1548013146-72479768bada?w=600&q=80',
        'delhi':              'https://images.unsplash.com/photo-1548013146-72479768bada?w=600&q=80',
        'kashmir':            'https://images.unsplash.com/photo-1566837945700-30057527ade0?w=600&q=80',
        'ladakh':             'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80',
        'ooty':               'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&q=80',
        'wayanad':            'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=600&q=80',
        'kollam':             'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80',
        'murudeshwar':        '/static/images/WebSites Images Travels/Murudeshwar Temple & Beach.webp',
    }
    _DEFAULT_IMAGE = 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&q=80'

    @property
    def image_src(self):
        """Returns uploaded image URL if available, else a keyword-matched Unsplash fallback."""
        if self.image:
            return self.image.url
        lower = self.name.lower()
        for key, url in self._FALLBACK_MAP.items():
            if key in lower:
                return url
        return self._DEFAULT_IMAGE

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='team/', blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    image = models.ImageField(upload_to='testimonials/', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    tour = models.ForeignKey('tours.TourPackage', on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tour')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} - {self.tour.title}"


class FAQ(models.Model):
    question = models.CharField(max_length=400)
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True, default='General')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question
