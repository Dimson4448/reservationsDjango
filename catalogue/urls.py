"""reservations.catalogue URL Configuration
"""
from django.urls import path

from . import views
from api.catalogue.views import (
    ArtistListCreateView,
    ArtistRetrieveUpdateDestroyView,
    RepresentationListView,
    ReservationCancelView,
    ReservationListCreateView,
    ReviewCreateView,
    ShowDetailView,
    ShowListView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'catalogue'

urlpatterns = [
    path('dashboard/', views.dashboard.index, name='dashboard-index'),
    path('dashboard/reservations/', views.dashboard.reservations, name='dashboard-reservations'),
    path('dashboard/reservations/<int:reservation_id>/status/', views.dashboard.update_reservation_status, name='dashboard-reservation-status'),
    path('dashboard/reviews/', views.dashboard.pending_reviews, name='dashboard-reviews'),
    path('dashboard/reviews/<int:review_id>/validate/', views.dashboard.validate_review, name='dashboard-review-validate'),
    path('dashboard/reservations/export/', views.dashboard.export_reservations, name='dashboard-reservations-export'),
    path('artist/', views.artist.index, name='artist-index'),
    path('artist/<int:artist_id>', views.artist.show, name='artist-show'),
    path('artist/edit/<int:artist_id>', views.artist.edit, name='artist-edit'),
    path('artist/create', views.artist.create, name='artist-create'),
    path('artist/delete/<int:artist_id>', views.artist.delete, name='artist-delete'),
    path('type/', views.type.index, name='type-index'),
    path('type/<int:type_id>', views.type.show, name='type-show'),
    path('locality/', views.locality.index, name='locality-index'),
    path('locality/<int:locality_id>', views.locality.show, name='locality-show'),
    path('price/', views.price.index, name='price-index'),
    path('price/<int:price_id>', views.price.show, name='price-show'),
    path('location/', views.location.index, name='location-index'),
    path('location/<int:location_id>', views.location.show, name='location-show'),
    path('show/', views.show_.index, name='show-index'),
    path('show/<int:show_id>', views.show_.show, name='show-show'),
    path('show/<int:show_id>/review', views.show_.add_review, name='show-review-create'),
    path('representation/<int:representation_id>/reserve', views.show_.reserve, name='reservation-create'),
    path('reservation/<int:reservation_id>/cart', views.show_.reservation_cart, name='reservation-cart'),
    path('reservation/<int:reservation_id>/payment', views.show_.start_payment, name='reservation-payment-start'),
    path('reservation/<int:reservation_id>/payment/success', views.show_.payment_success, name='reservation-payment-success'),
    path('payment/stripe/webhook/', views.show_.stripe_webhook, name='stripe-webhook'),
    path('reservation/<int:reservation_id>/confirmation', views.show_.reservation_confirmation, name='reservation-confirmation'),
    path('reservation/<int:reservation_id>/ticket', views.show_.reservation_ticket, name='reservation-ticket'),
    path('reservation/<int:reservation_id>/cancel', views.show_.cancel_reservation, name='reservation-cancel'),
    path('representation/', views.representation.index, name='representation-index'),
    path('representation/<int:representation_id>', views.representation.show, name='representation-show'),

    path('api/artists/', ArtistListCreateView.as_view(), name='artist-list'),
    path('api/artists/<int:pk>/', ArtistRetrieveUpdateDestroyView.as_view(), name='artist-detail'),
    path('api/shows/', ShowListView.as_view(), name='api-show-list'),
    path('api/shows/<int:pk>/', ShowDetailView.as_view(), name='api-show-detail'),
    path('api/representations/', RepresentationListView.as_view(), name='api-representation-list'),
    path('api/reservations/', ReservationListCreateView.as_view(), name='api-reservation-list'),
    path('api/reservations/<int:pk>/cancel/', ReservationCancelView.as_view(), name='api-reservation-cancel'),
    path('api/shows/<int:show_id>/reviews/', ReviewCreateView.as_view(), name='api-review-create'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
