from rest_framework import viewsets, mixins, status, generics
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
import logging
from .serializers import ContactSerializer, NewsletterSerializer, ContactDetailSerializer
from .models import Contact, Newsletter, Company_info
from .tasks import send_contact_emails
from rest_framework.views import APIView
logger = logging.getLogger(__name__)

class ContactViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = []

    @extend_schema(
    tags=["Contact"],
    summary="Submit contact form",
    description="Sends contact message to admin email",
        request=ContactSerializer,
        responses={201: ContactSerializer},
        examples=[
            OpenApiExample(
                "Contact Example",
                value={
                    "full_name": "Sanjeet Thapa Magar",
                    "email": "sanjeet@example.com",
                    "phone": "+977-9812345678",
                    "subject": "Collaboration Inquiry",
                    "message": "Hello, I'd like to collaborate with your college.",
                },
            ),
        ],
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        try:
            contact_obj = serializer.save()
            logger.info(f"Contact saved: {contact_obj.id} - {contact_obj.email}")

            # Send email async
            send_contact_emails.delay(
                contact_obj.id,
                contact_obj.full_name,
                contact_obj.email,
                contact_obj.phone,
                contact_obj.subject,
                contact_obj.message,
            )

            return Response(
                {
                    "message": "Message received successfully! We'll contact you soon.",
                    "contact_id": contact_obj.id,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception:
            logger.exception("Error saving contact")
            return Response(
                {"error": "Server error, please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

@extend_schema(tags=["Contact"])
class NewsletterViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    pagination_class = None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            error_message = serializer.errors.get("email", ["Invalid data"])[0]
            return Response(
                {  "email": ["your email is already subscribed to the newsletter"]},
            )

        newsletter_obj = serializer.save()

        return Response(
            {
                "message": "Subscribed successfully!",
                "newsletter_id": newsletter_obj.id,
            },
            status=status.HTTP_201_CREATED
        )

@extend_schema(tags=["Contact"])
class ContactDetailView(APIView):
    def get(self, request):
        company = Company_info.objects.first()
        serializer = ContactDetailSerializer(company)
        return Response(serializer.data)