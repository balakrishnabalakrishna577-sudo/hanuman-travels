"""
Management command to load sample data for Hanuman Tours and Travels.
Run: python manage.py load_sample_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Destination, Testimonial, TeamMember
from tours.models import TourPackage, IncludedService, ExcludedService, Itinerary
from gallery.models import GalleryCategory, GalleryImage
from blog.models import BlogCategory, BlogPost
from vehicles.models import Vehicle
from hotels.models import Hotel, RoomType
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Load sample data for the website'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading sample data...')

        # Destinations
        destinations_data = [
            # Original
            ('Goa', 'India', 'Goa', True),
            ('Kerala', 'India', 'Kerala', True),
            ('Rajasthan', 'India', 'Rajasthan', True),
            ('Himachal Pradesh', 'India', 'Himachal Pradesh', True),
            ('Andaman Islands', 'India', 'Andaman & Nicobar', True),
            ('Varanasi', 'India', 'Uttar Pradesh', True),
            ('Manali', 'India', 'Himachal Pradesh', True),
            ('Ooty', 'India', 'Tamil Nadu', True),
            # South India & Pilgrimage Circuit
            ('Kanyakumari', 'India', 'Tamil Nadu', True),
            ('Rameswaram', 'India', 'Tamil Nadu', True),
            ('Madurai', 'India', 'Tamil Nadu', True),
            ('Palani', 'India', 'Tamil Nadu', True),
            ('Sigandur', 'India', 'Karnataka', True),
            ('Jog Falls', 'India', 'Karnataka', True),
            ('Honnavar', 'India', 'Karnataka', True),
            ('Om Beach', 'India', 'Karnataka', True),
            ('Malpe Beach', 'India', 'Karnataka', True),
            ('Udupi', 'India', 'Karnataka', True),
            ('Wayanad', 'India', 'Kerala', True),
            ('Kukke Subramanya', 'India', 'Karnataka', True),
            ('Sakleshpur', 'India', 'Karnataka', True),
            ('Halebidu', 'India', 'Karnataka', True),
            ('Belur', 'India', 'Karnataka', True),
            ('Chikkamagaluru', 'India', 'Karnataka', True),
            ('Jatayu Park', 'India', 'Kerala', True),
            ('Guruvayur', 'India', 'Kerala', True),
            ('Irinjalakuda', 'India', 'Kerala', True),
            ('Pampa', 'India', 'Kerala', True),
            ('Sabarimala', 'India', 'Kerala', True),
            ('Spondylus', 'India', 'Kerala', True),
            ('Thiruvananthapuram', 'India', 'Kerala', True),
            ('Kollam Beach', 'India', 'Kerala', True),
            ('Hajmala', 'India', 'Kerala', True),
            ('Kudremukh', 'India', 'Karnataka', True),
            ('Gokarna', 'India', 'Karnataka', True),
            ('Murudeshwar Beach', 'India', 'Karnataka', True),
            ('Mullayanagiri', 'India', 'Karnataka', True),
            ('Baba Budangiri', 'India', 'Karnataka', True),
        ]
        destinations = {}
        for name, country, state, popular in destinations_data:
            slug = slugify(name)
            dest, _ = Destination.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'country': country, 'state': state,
                          'description': f'Beautiful destination - {name}', 'is_popular': popular}
            )
            destinations[name] = dest

        # Tour Packages
        packages_data = [
            # Original
            ('Goa Beach Paradise', 'Goa', 5, 4, 12999, 9999, 'beach', True),
            ('Kerala Backwaters Tour', 'Kerala', 7, 6, 18999, 15999, 'cultural', True),
            ('Rajasthan Royal Tour', 'Rajasthan', 10, 9, 25999, 22999, 'cultural', True),
            ('Manali Snow Adventure', 'Manali', 6, 5, 15999, 12999, 'adventure', True),
            ('Andaman Island Escape', 'Andaman Islands', 8, 7, 35999, 29999, 'beach', True),
            ('Varanasi Spiritual Tour', 'Varanasi', 4, 3, 8999, None, 'religious', False),
            # New destinations
            ('Kanyakumari Sunrise Tour', 'Kanyakumari', 3, 2, 7999, 6499, 'religious', True),
            ('Rameswaram Pilgrimage', 'Rameswaram', 3, 2, 6999, 5499, 'religious', True),
            ('Madurai Temple Tour', 'Madurai', 2, 1, 4999, 3999, 'religious', True),
            ('Palani Murugan Darshan', 'Palani', 2, 1, 4499, 3499, 'religious', False),
            ('Sigandur Forest Trek', 'Sigandur', 2, 1, 5999, 4999, 'adventure', True),
            ('Jog Falls Nature Trip', 'Jog Falls', 2, 1, 4999, 3999, 'hill', True),
            ('Honnavar Coastal Escape', 'Honnavar', 3, 2, 6499, 5499, 'beach', True),
            ('Om Beach Gokarna Tour', 'Om Beach', 3, 2, 7499, 5999, 'beach', True),
            ('Malpe Beach Holiday', 'Malpe Beach', 2, 1, 5499, 4499, 'beach', True),
            ('Udupi Krishna Darshan', 'Udupi', 2, 1, 4999, 3999, 'religious', True),
            ('Wayanad Wildlife Safari', 'Wayanad', 3, 2, 8999, 7499, 'wildlife', True),
            ('Kukke Subramanya Darshan', 'Kukke Subramanya', 2, 1, 4499, 3499, 'religious', True),
            ('Sakleshpur Coffee Trail', 'Sakleshpur', 2, 1, 5999, 4999, 'hill', True),
            ('Halebidu Heritage Tour', 'Halebidu', 2, 1, 4999, 3999, 'cultural', True),
            ('Belur Temple Tour', 'Belur', 2, 1, 4999, 3999, 'cultural', True),
            ('Chikkamagaluru Hill Retreat', 'Chikkamagaluru', 3, 2, 7999, 6499, 'hill', True),
            ('Jatayu Park Adventure', 'Jatayu Park', 2, 1, 5999, 4999, 'adventure', True),
            ('Guruvayur Temple Tour', 'Guruvayur', 2, 1, 4999, 3999, 'religious', True),
            ('Sabarimala Pilgrimage', 'Sabarimala', 3, 2, 6999, 5499, 'religious', True),
            ('Pampa River Pilgrimage', 'Pampa', 2, 1, 5499, 4499, 'religious', False),
            ('Thiruvananthapuram City Tour', 'Thiruvananthapuram', 3, 2, 7499, 5999, 'cultural', True),
            ('Kollam Beach Retreat', 'Kollam Beach', 2, 1, 5499, 4499, 'beach', True),
            ('Hajmala Spiritual Tour', 'Hajmala', 2, 1, 4499, 3499, 'religious', False),
            ('Kudremukh Trek', 'Kudremukh', 3, 2, 8499, 6999, 'adventure', True),
            ('Gokarna Beach Pilgrimage', 'Gokarna', 3, 2, 6999, 5499, 'beach', True),
            ('Murudeshwar Temple & Beach', 'Murudeshwar Beach', 2, 1, 5999, 4999, 'religious', True),
            ('Mullayanagiri Peak Trek', 'Mullayanagiri', 2, 1, 5499, 4499, 'adventure', True),
            ('Baba Budangiri Pilgrimage', 'Baba Budangiri', 2, 1, 4999, 3999, 'religious', True),
        ]
        for title, dest_name, days, nights, price, disc_price, tour_type, featured in packages_data:
            pkg, created = TourPackage.objects.get_or_create(
                title=title,
                defaults={
                    'slug': slugify(title),
                    'destination': destinations.get(dest_name, list(destinations.values())[0]),
                    'duration_days': days,
                    'duration_nights': nights,
                    'price_per_person': price,
                    'discounted_price': disc_price,
                    'tour_type': tour_type,
                    'is_featured': featured,
                    'is_active': True,
                    'description': f'Experience the best of {dest_name} with our carefully crafted {title} package.',
                    'highlights': f'Visit top attractions\nExpert local guide\nComfortable accommodation\nAll meals included\nTransportation provided',
                    'max_group_size': 20,
                    'min_age': 5,
                }
            )
            if created:
                IncludedService.objects.create(tour=pkg, item='Accommodation (Hotel/Resort)')
                IncludedService.objects.create(tour=pkg, item='All Meals (Breakfast, Lunch, Dinner)')
                IncludedService.objects.create(tour=pkg, item='Transportation (AC Vehicle)')
                IncludedService.objects.create(tour=pkg, item='Expert Tour Guide')
                ExcludedService.objects.create(tour=pkg, item='Flight Tickets')
                ExcludedService.objects.create(tour=pkg, item='Personal Expenses')
                ExcludedService.objects.create(tour=pkg, item='Travel Insurance')
                for day in range(1, days + 1):
                    Itinerary.objects.create(
                        tour=pkg, day=day,
                        title=f'Day {day} - Explore {dest_name}',
                        description=f'Today we explore the beautiful sights of {dest_name}. Enjoy local cuisine and culture.',
                        meals='Breakfast, Lunch, Dinner',
                        accommodation='Hotel/Resort'
                    )

        # Testimonials
        testimonials_data = [
            ('Rahul Sharma', 'Delhi', 'Amazing experience! The Goa tour was perfectly organized. Highly recommend Hanuman Tours!', 5),
            ('Priya Patel', 'Mumbai', 'Kerala backwaters tour was breathtaking. The team was very professional and caring.', 5),
            ('Amit Kumar', 'Bangalore', 'Best travel agency in Hyderabad. Rajasthan tour exceeded all expectations!', 5),
            ('Sunita Reddy', 'Hyderabad', 'Manali trip was unforgettable. Great service, great price, great memories!', 4),
            ('Vikram Singh', 'Chennai', 'Andaman tour was a dream come true. Everything was well planned and executed.', 5),
            ('Meera Joshi', 'Pune', 'Excellent service from booking to return. Will definitely book again!', 5),
        ]
        for name, location, message, rating in testimonials_data:
            Testimonial.objects.get_or_create(
                name=name,
                defaults={'location': location, 'message': message, 'rating': rating, 'is_active': True}
            )

        # Team Members
        team_data = [
            ('Rajesh Hanuman', 'Founder & CEO', 'With 15+ years in travel industry, Rajesh leads our team with passion.', 1),
            ('Priya Sharma', 'Operations Manager', 'Priya ensures every tour runs smoothly and customers are happy.', 2),
            ('Arun Kumar', 'Tour Guide Expert', 'Arun has guided 500+ tours across India with expertise.', 3),
            ('Kavitha Reddy', 'Customer Relations', 'Kavitha is dedicated to providing the best customer experience.', 4),
        ]
        for name, designation, bio, order in team_data:
            TeamMember.objects.get_or_create(
                name=name,
                defaults={'designation': designation, 'bio': bio, 'order': order}
            )

        # Vehicles
        vehicles_data = [
            ('Toyota Innova', 'suv', 'Innova Crysta 2023', 7, 2500, True),
            ('Tempo Traveller', 'tempo', 'Force Tempo 2022', 12, 4000, True),
            ('Maruti Swift Dzire', 'sedan', 'Swift Dzire 2023', 4, 1500, True),
            ('Luxury Mercedes', 'luxury', 'Mercedes E-Class', 4, 8000, True),
            ('Mini Bus', 'bus', 'Tata Winger 2022', 20, 7000, True),
        ]
        for name, vtype, model, capacity, price, ac in vehicles_data:
            Vehicle.objects.get_or_create(
                name=name,
                defaults={
                    'vehicle_type': vtype, 'model': model, 'capacity': capacity,
                    'price_per_day': price, 'is_ac': ac, 'driver_included': True,
                    'is_available': True,
                    'features': 'AC\nMusic System\nFirst Aid Kit\nGPS Navigation',
                    'description': f'Comfortable {name} for your travel needs.'
                }
            )

        # Gallery Categories
        for cat_name in ['Destinations', 'Tour Moments', 'Wildlife', 'Beaches', 'Mountains']:
            GalleryCategory.objects.get_or_create(name=cat_name, defaults={'slug': slugify(cat_name)})

        # Blog Categories
        for cat_name in ['Travel Tips', 'Destinations', 'Food & Culture', 'Adventure', 'Budget Travel']:
            BlogCategory.objects.get_or_create(name=cat_name, defaults={'slug': slugify(cat_name)})

        # Sample Blog Posts
        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user:
            blog_cat = BlogCategory.objects.first()
            posts_data = [
                ('Top 10 Places to Visit in Goa', 'goa-top-10', 'Discover the best beaches, churches and nightlife in Goa.', 'Goa is one of India\'s most popular tourist destinations...'),
                ('Kerala Backwaters: A Complete Guide', 'kerala-backwaters-guide', 'Everything you need to know about Kerala backwaters.', 'The backwaters of Kerala are a network of interconnected canals...'),
                ('Budget Travel Tips for India', 'budget-travel-india', 'How to travel India on a budget without compromising on experience.', 'India is a vast country with diverse experiences...'),
            ]
            for title, slug, excerpt, content in posts_data:
                BlogPost.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'title': title, 'author': admin_user, 'category': blog_cat,
                        'excerpt': excerpt, 'content': content, 'is_published': True
                    }
                )

        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
        self.stdout.write('Admin: username=admin, password=admin123')
        self.stdout.write('Run: python manage.py runserver')
