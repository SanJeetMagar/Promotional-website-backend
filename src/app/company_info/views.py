from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from .models import TeamCategory, TeamMember, AboutPage, JourneyMilestone
from .serializers import TeamCategorySerializer, TeamMemberSerializer, AboutPageSerializer, JourneyMilestoneSerializer


# ------------------------------
# 1) LIST ALL TEAM CATEGORIES
# ------------------------------
@extend_schema(
    tags=["Team"],
    summary="Get all team categories",
    description="Returns a list of all team categories such as Leadership, Design, Development, etc.",
)
class TeamCategoryListView(ListAPIView):
    queryset = TeamCategory.objects.all().order_by("title")
    serializer_class = TeamCategorySerializer
    pagination_class = None



# ------------------------------
# 2) LIST TEAM MEMBERS (FILTER BY CATEGORY SLUG)
# ------------------------------
@extend_schema(
    tags=["Team"],)
class TeamMemberListView(ListAPIView):
    serializer_class = TeamMemberSerializer
    pagination_class = None


    @extend_schema(
        summary="Get team members by category",
        description="Returns team members filtered by category slug. Example: ?team=leadership",
        parameters=[
            OpenApiParameter(
                name="team",
                description="Category slug (e.g. leadership, design, marketing)",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY
            ),
        ],
    )
    def get_queryset(self):
        qs = TeamMember.objects.all().select_related("team")
        team_slug = self.request.query_params.get("team")

        if team_slug:
            qs = qs.filter(team__slug=team_slug)

        return qs


# ------------------------------
# 3) GET ABOUT PAGE DATA
# ------------------------------
@extend_schema(
    tags=["About"],
    summary="Get about page data",
    description="Returns hero images and paragraphs for the about page",
)
class AboutPageView(RetrieveAPIView):
    serializer_class = AboutPageSerializer
    pagination_class = None

    def get_object(self):
        """Return the first/main about page, create if doesn't exist"""
        obj, created = AboutPage.objects.get_or_create(
            id=1,
            defaults={"title": "About Choongshin"}
        )
        return obj


# ------------------------------
# 4) LIST JOURNEY MILESTONES
# ------------------------------
@extend_schema(
    tags=["About"],
    summary="Get company journey milestones",
    description="Returns a timeline of company milestones from founding to present",
)
class JourneyMilestoneListView(ListAPIView):
    queryset = JourneyMilestone.objects.all().order_by("order")
    serializer_class = JourneyMilestoneSerializer
    pagination_class = None
