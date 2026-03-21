from django.db import models
from django.contrib.auth.models import User
from tours.models import TourPackage


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]

    booking_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    tour = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='bookings')
    travel_date = models.DateField()
    num_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    payment_id = models.CharField(max_length=200, blank=True)
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.booking_id:
            import random, string
            self.booking_id = 'HT' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id} - {self.user.username} - {self.tour.title}"

    class Meta:
        ordering = ['-created_at']


class TravelerDetail(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='travelers')
    name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    id_type = models.CharField(max_length=50, choices=[
        ('aadhar', 'Aadhar Card'),
        ('passport', 'Passport'),
        ('driving', 'Driving License'),
        ('voter', 'Voter ID'),
    ])
    id_number = models.CharField(max_length=100)

    def __str__(self):
        return self.name
