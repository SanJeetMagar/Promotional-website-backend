from rest_framework import serializers
from .models import Contact, Newsletter, Company_info, Tagline


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ["id", "email", "created_at"]

    def validate_email(self, value):
        if Newsletter.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Your email is already subscribed to the newsletter"
            )
        return value


class TaglineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tagline
        fields = ["id", "text"] 


class ContactDetailSerializer(serializers.ModelSerializer):
    taglines = TaglineSerializer(many=True, read_only=True)

    class Meta:
        model = Company_info
        fields = "__all__"
