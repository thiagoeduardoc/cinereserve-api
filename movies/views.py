from rest_framework import generics, permissions
from .models import Movie
from .serializers import MovieSerializer
 
 
class MovieListView(generics.ListAPIView):
    serializer_class   = MovieSerializer
    permission_classes = [permissions.AllowAny]

    queryset = Movie.objects.filter(is_active=True)
    
 