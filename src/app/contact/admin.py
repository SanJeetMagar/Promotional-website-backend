from django.contrib import admin
from .models import Company_info, Tagline




class TaglineInline(admin.TabularInline):
    model = Tagline
    extra = 1   # allow adding many taglines


class CompanyAdmin(admin.ModelAdmin):
    inlines = [TaglineInline]

    def has_add_permission(self, request):
        # Allow adding only if no company exists
        return Company_info.objects.count() < 1


admin.site.register(Company_info, CompanyAdmin)
