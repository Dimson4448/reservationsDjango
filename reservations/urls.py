from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('catalogue/', include('catalogue.urls')),
    path('admin/', admin.site.urls),
]

admin.site.index_title = "Projet Réservations"
admin.site.index_header = "Projet Réservations HEADER"
admin.site.site_title = "Spectacles"

