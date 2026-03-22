from rest_framework import generics, permissions
from .models import Session
from .serializers import SessionSerializer
 
 
class SessionListView(generics.ListAPIView):
    serializer_class   = SessionSerializer
    permission_classes = [permissions.AllowAny]

    queryset = Session.objects.all()
 
    def get_queryset(self):
        return super().get_queryset().filter(movie_id=self.kwargs['movie_id'])
 