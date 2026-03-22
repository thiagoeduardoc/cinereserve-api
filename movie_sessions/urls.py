from django.urls import path
from .views import SessionListView, SeatListView, ReserveView, PurchaseView, MyReservationsView, MyTicketsView

urlpatterns = [
    path('<int:movie_id>/sessions/', SessionListView.as_view(), name='session-list'),
    path('sessions/<int:session_id>/seats/', SeatListView.as_view(),   name='seat-list'),
    path('sessions/<int:session_id>/seats/<int:seat_id>/reserve/', ReserveView.as_view(), name='seat-reserve'),
    path('sessions/<int:session_id>/seats/<int:seat_id>/purchase/', PurchaseView.as_view(), name='seat-purchase'),
    path('my-reservations/', MyReservationsView.as_view(),  name='my-reservations'),
    path('my-tickets/', MyTicketsView.as_view(),  name='my-tickets'),
]