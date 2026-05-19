from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from .views import health_check

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('health/', health_check, name='health-check'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('catalogue/', include('catalogue.urls')),

    # Routes de reinitialisation du mot de passe pour l'administration
    path(
        "admin/password_reset/",
        auth_views.PasswordResetView.as_view(
            extra_context={"site_header": admin.site.site_header}
        ),
        name="admin_password_reset",
    ),
    path(
        "admin/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            extra_context={"site_header": admin.site.site_header}
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            extra_context={"site_header": admin.site.site_header}
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            extra_context={"site_header": admin.site.site_header}
        ),
        name="password_reset_complete",
    ),

    # Route vers l'administration Django
    path('admin/', admin.site.urls),
]

admin.site.site_header = "Ultimate SPT Administration"
admin.site.index_title = "Pilotage des spectacles"
admin.site.site_title = "Ultimate SPT Admin"
