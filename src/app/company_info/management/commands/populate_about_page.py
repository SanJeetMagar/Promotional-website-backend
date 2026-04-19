from django.core.management.base import BaseCommand
from src.app.company_info.models import HeroImage, AboutPage, JourneyMilestone


class Command(BaseCommand):
    help = "Populate the about page with initial hero images, paragraphs, and journey milestones"

    def handle(self, *args, **options):
        # Hero images data
        hero_images_data = [
            {
                "url": "https://www.gitagged.com/wp-content/uploads/2018/07/Wooden-Art-Gi-Tagged-1.jpg",
                "alt_text": "Wooden Art",
                "order": 0,
            },
            {
                "url": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=600&auto=format&fit=crop",
                "alt_text": "Artisan craftsmanship",
                "order": 1,
            },
            {
                "url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&auto=format&fit=crop",
                "alt_text": "Handmade details",
                "order": 2,
            },
            {
                "url": "https://images.unsplash.com/photo-1604014237800-1c9102c219da?w=600&auto=format&fit=crop",
                "alt_text": "Workshop inspiration",
                "order": 3,
            },
            {
                "url": "https://images.unsplash.com/photo-1611486212557-88be5ff6f941?w=600&auto=format&fit=crop",
                "alt_text": "Creative process",
                "order": 4,
            },
            {
                "url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=600&auto=format&fit=crop",
                "alt_text": "Artistic vision",
                "order": 5,
            },
            {
                "url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8?w=600&auto=format&fit=crop",
                "alt_text": "Quality materials",
                "order": 6,
            },
            {
                "url": "https://images.unsplash.com/photo-1481349518771-20055b2a7b24?w=600&auto=format&fit=crop",
                "alt_text": "Finished products",
                "order": 7,
            },
        ]

        # Paragraphs data
        paragraphs_data = [
            {
                "text": "Founded in the heart of artisan country, Choongshin represents more than just a company—we are a movement to preserve and celebrate the art of handcrafted excellence.",
                "highlight": False,
            },
            {
                "text": "Our name, meaning sincerity in Korean, embodies our commitment to authentic craftsmanship. Every product we create tells a story. From the selection of premium materials to the final touches by master artisans, we ensure that each piece meets our exacting standards.",
                "highlight": False,
            },
            {
                "text": "Our workshop is a place where tradition and innovation dance together, creating gifts that are both timeless and contemporary. We believe in the power of meaningful gifts—items that carry emotional weight, cultural significance, and unparalleled quality.",
                "highlight": False,
            },
            {
                "text": "In a world of mass production, we stand firm in our dedication to the human touch, fair trade practices, and sustainable craftsmanship that honors both people and planet.",
                "highlight": True,  # This one has highlight (bold in frontend)
            },
        ]

        # Journey milestones data
        journey_milestones_data = [
            {
                "year": "2015",
                "title": "The Beginning",
                "description": "Founded with a vision to preserve traditional craftsmanship and support local artisans in their craft.",
                "order": 0,
            },
            {
                "year": "2017",
                "title": "Artisan Network",
                "description": "Partnered with 50+ master craftspeople across multiple regions, creating a thriving community.",
                "order": 1,
            },
            {
                "year": "2019",
                "title": "Global Recognition",
                "description": "Received international awards for design excellence and commitment to preserving cultural heritage.",
                "order": 2,
            },
            {
                "year": "2021",
                "title": "Sustainable Practice",
                "description": "Committed to eco-friendly materials, ethical sourcing, and zero-waste production methods.",
                "order": 3,
            },
            {
                "year": "2023",
                "title": "Digital Innovation",
                "description": "Launched online platform connecting artisans with customers worldwide, bridging tradition and technology.",
                "order": 4,
            },
            {
                "year": "2025",
                "title": "Expanding Horizons",
                "description": "Opening new workshops, training programs, and mentorship initiatives for the next generation.",
                "order": 5,
            },
        ]

        # Create or clear hero images
        HeroImage.objects.all().delete()
        created_images = []
        for image_data in hero_images_data:
            image, created = HeroImage.objects.get_or_create(
                url=image_data["url"],
                defaults={
                    "alt_text": image_data["alt_text"],
                    "order": image_data["order"],
                },
            )
            created_images.append(image)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created hero image: {image.alt_text}")
                )

        # Create or update about page
        about_page, created = AboutPage.objects.get_or_create(
            id=1,
            defaults={
                "title": "About Choongshin",
                "paragraphs": paragraphs_data,
            },
        )

        if not created:
            about_page.paragraphs = paragraphs_data
            about_page.save()

        # Add hero images to about page
        about_page.hero_images.set(created_images)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully populated about page with {len(created_images)} hero images and {len(paragraphs_data)} paragraphs"
            )
        )

        # Create or clear journey milestones
        JourneyMilestone.objects.all().delete()
        for milestone_data in journey_milestones_data:
            milestone, created = JourneyMilestone.objects.get_or_create(
                year=milestone_data["year"],
                defaults={
                    "title": milestone_data["title"],
                    "description": milestone_data["description"],
                    "order": milestone_data["order"],
                },
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created milestone: {milestone.year} - {milestone.title}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully populated {len(journey_milestones_data)} journey milestones"
            )
        )
