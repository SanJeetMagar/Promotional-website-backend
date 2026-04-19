from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # API documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema")),

    # Your existing APIs
    path("api/v1/", include("src.app.contact.urls")),
    path("api/v1/", include("src.app.products.urls")),
    path("api/v1/", include("src.app.gallery.urls")),
    path("api/v1/", include("src.app.company_info.urls")),
    path("api/v1/faq/",include("src.app.faq.urls")),
    path("api/v1/", include("src.app.homepage.urls")),
    path("api/v1/collab/", include("src.app.collab.urls")),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
