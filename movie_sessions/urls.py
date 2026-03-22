from django.urls import path
from .views import SessionListView, SeatListView, ReserveView, MyTicketsView

urlpatterns = [
    path('<int:movie_id>/sessions/', SessionListView.as_view(), name='session-list'),
    path('sessions/<int:session_id>/seats/', SeatListView.as_view(),   name='seat-list'),
    path('sessions/<int:session_id>/seats/<int:seat_id>/reserve/', ReserveView.as_view(), name='seat-reserve'),
    path('my-tickets/', MyTicketsView.as_view(),  name='my-tickets'),
]