from django.db import models
from django.contrib.auth.models import User


class Vehicle(models.Model):
    TYPE_CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('tempo', 'Tempo Traveller'),
        ('bus', 'Bus'),
        ('luxury', 'Luxury Car'),
        ('bike', 'Bike'),
    ]

    name = models.CharField(max_length=200)
    vehicle_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    model = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_km = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    image = models.ImageField(upload_to='vehicles/')
    features = models.TextField(blank=True, help_text='One feature per line')
    is_ac = models.BooleanField(default=True)
    driver_included = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.vehicle_type})"

    class Meta:
        ordering = ['price_per_day']


class CarBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    booking_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='car_bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    pickup_location = models.CharField(max_length=300)
    drop_location = models.CharField(max_length=300)
    pickup_date = models.DateField()
    return_date = models.DateField()
    with_driver = models.BooleanField(default=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.booking_id:
            import random, string
            self.booking_id = 'CB' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id} - {self.vehicle.name}"

    class Meta:
        ordering = ['-created_at']


class AirportTransfer(models.Model):
    TRANSFER_CHOICES = [
        ('pickup', 'Airport Pickup'),
        ('drop', 'Airport Drop'),
        ('both', 'Both Pickup & Drop'),
    ]
    VEHICLE_CHOICES = [
        ('sedan', 'Sedan (1-4 pax)'),
        ('suv', 'SUV (1-6 pax)'),
        ('tempo', 'Tempo Traveller (7-12 pax)'),
        ('bus', 'Mini Bus (13-20 pax)'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    PAYMENT_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]

    booking_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='airport_transfers')
    transfer_type = models.CharField(max_length=10, choices=TRANSFER_CHOICES)
    airport_name = models.CharField(max_length=200)
    flight_number = models.CharField(max_length=20, blank=True)
    passenger_name = models.CharField(max_length=200)
    passenger_phone = models.CharField(max_length=20)
    passenger_email = models.EmailField()
    pickup_address = models.TextField()
    drop_address = models.TextField()
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    return_date = models.DateField(null=True, blank=True)
    return_time = models.TimeField(null=True, blank=True)
    passengers = models.PositiveIntegerField(default=1)
    luggage_count = models.PositiveIntegerField(default=1)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.booking_id:
            import random, string
            self.booking_id = 'AT' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id} - {self.passenger_name} ({self.get_transfer_type_display()})"

    class Meta:
        ordering = ['-created_at']
