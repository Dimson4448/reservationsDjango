from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('catalogue/', include('catalogue.urls')),
    path('admin/', admin.site.urls),
]
