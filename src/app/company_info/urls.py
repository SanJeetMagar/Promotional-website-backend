from django.urls import path
from .views import TeamCategoryListView, TeamMemberListView, AboutPageView, JourneyMilestoneListView

urlpatterns = [
    path("team-list/", TeamCategoryListView.as_view(), name="team-list"),
    path("team-members/", TeamMemberListView.as_view(), name="team-members"),
    path("about/", AboutPageView.as_view(), name="about-page"),
    path("journey/", JourneyMilestoneListView.as_view(), name="journey-milestones"),
]
