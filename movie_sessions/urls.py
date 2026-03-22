from django.urls import path
from .views import SessionListView
 
urlpatterns = [
    path('<int:movie_id>/sessions/', SessionListView.as_view(), name='session-list'),
]