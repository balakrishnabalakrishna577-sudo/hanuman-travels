from django.db import models
from django.contrib.auth.models import User
from core.models import Destination


class TourPackage(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('challenging', 'Challenging'),
    ]
    TYPE_CHOICES = [
        ('adventure', 'Adventure'),
        ('cultural', 'Cultural'),
        ('religious', 'Religious'),
        ('beach', 'Beach'),
        ('hill', 'Hill Station'),
        ('wildlife', 'Wildlife'),
        ('honeymoon', 'Honeymoon'),
        ('family', 'Family'),
    ]

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='packages')
    tour_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='cultural')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='easy')
    description = models.TextField()
    highlights = models.TextField(help_text='One highlight per line')
    duration_days = models.PositiveIntegerField()
    duration_nights = models.PositiveIntegerField()
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_group_size = models.PositiveIntegerField(default=20)
    min_age = models.PositiveIntegerField(default=5)
    thumbnail = models.ImageField(upload_to='tours/thumbnails/', blank=True)
    thumbnail_url = models.URLField(blank=True, help_text='Auto-filled image URL (used when no file is uploaded)')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def final_price(self):
        return self.discounted_price if self.discounted_price else self.price_per_person

    @property
    def image_src(self):
        """Returns the best available image URL for this tour."""
        if self.thumbnail:
            return self.thumbnail.url
        if self.thumbnail_url:
            return self.thumbnail_url
        # Fall back to destination image
        if self.destination_id:
            return self.destination.image_src
        return 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&q=80'

    @property
    def discount_percent(self):
        if self.discounted_price:
            return int(((self.price_per_person - self.discounted_price) / self.price_per_person) * 100)
        return 0

    @property
    def avg_rating(self):
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0

    class Meta:
        ordering = ['-created_at']


class TourImage(models.Model):
    tour = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='tours/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tour.title} - Image"


class Itinerary(models.Model):
    tour = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='itinerary')
    day = models.PositiveIntegerField()
    title = models.CharField(max_length=300)
    description = models.TextField()
    meals = models.CharField(max_length=200, blank=True, help_text='e.g. Breakfast, Lunch, Dinner')
    accommodation = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Day {self.day}: {self.title}"

    class Meta:
        ordering = ['day']


class IncludedService(models.Model):
    tour = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='included')
    item = models.CharField(max_length=300)

    def __str__(self):
        return self.item


class ExcludedService(models.Model):
    tour = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='excluded')
    item = models.CharField(max_length=300)

    def __str__(self):
        return self.item


class Review(models.Model):
    tour = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.tour.title} ({self.rating}★)"

    class Meta:
        ordering = ['-created_at']
        unique_together = ['tour', 'user']
