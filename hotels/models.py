from django.db import models
from django.contrib.auth.models import User
from core.models import Destination


class Hotel(models.Model):
    STAR_CHOICES = [(i, f'{i} Star') for i in range(1, 6)]

    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='hotels')
    stars = models.PositiveSmallIntegerField(choices=STAR_CHOICES, default=3)
    description = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    image = models.ImageField(upload_to='hotels/')
    amenities = models.TextField(blank=True, help_text='One amenity per line')
    check_in_time = models.TimeField(default='14:00')
    check_out_time = models.TimeField(default='11:00')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-stars', 'name']


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(default=2)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='hotels/rooms/', blank=True)
    amenities = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.name}"


class HotelBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    booking_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hotel_bookings')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='bookings')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    num_rooms = models.PositiveIntegerField(default=1)
    num_guests = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.booking_id:
            import random, string
            self.booking_id = 'HB' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id} - {self.hotel.name}"

    class Meta:
        ordering = ['-created_at']
