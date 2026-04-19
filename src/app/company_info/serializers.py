from rest_framework import serializers
from .models import TeamCategory, TeamMember, HeroImage, AboutPage, JourneyMilestone


class TeamCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamCategory
        fields = ["id", "title", "slug"]


class TeamMemberSerializer(serializers.ModelSerializer):
    team = serializers.CharField(source="team.title")

    class Meta:
        model = TeamMember
        fields = [
            "id",
            "name",
            "position",
            "bio",
            # "badge_name"\,
            "image_url",
            "team",
        ]


class HeroImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroImage
        fields = ["id", "url", "alt_text", "order"]


class AboutPageSerializer(serializers.ModelSerializer):
    hero_images = HeroImageSerializer(many=True, read_only=True)

    class Meta:
        model = AboutPage
        fields = ["id", "title", "paragraphs", "hero_images"]


class JourneyMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneyMilestone
        fields = ["id", "year", "title", "description", "order"]
