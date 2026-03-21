from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AirportTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.CharField(editable=False, max_length=20, unique=True)),
                ('transfer_type', models.CharField(choices=[('pickup', 'Airport Pickup'), ('drop', 'Airport Drop'), ('both', 'Both Pickup & Drop')], max_length=10)),
                ('airport_name', models.CharField(max_length=200)),
                ('flight_number', models.CharField(blank=True, max_length=20)),
                ('passenger_name', models.CharField(max_length=200)),
                ('passenger_phone', models.CharField(max_length=20)),
                ('passenger_email', models.EmailField()),
                ('pickup_address', models.TextField()),
                ('drop_address', models.TextField()),
                ('pickup_date', models.DateField()),
                ('pickup_time', models.TimeField()),
                ('return_date', models.DateField(blank=True, null=True)),
                ('return_time', models.TimeField(blank=True, null=True)),
                ('passengers', models.PositiveIntegerField(default=1)),
                ('luggage_count', models.PositiveIntegerField(default=1)),
                ('vehicle_type', models.CharField(choices=[('sedan', 'Sedan (1-4 pax)'), ('suv', 'SUV (1-6 pax)'), ('tempo', 'Tempo Traveller (7-12 pax)'), ('bus', 'Mini Bus (13-20 pax)')], max_length=20)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('special_requests', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='pending', max_length=20)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('refunded', 'Refunded')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='airport_transfers', to='auth.user')),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
