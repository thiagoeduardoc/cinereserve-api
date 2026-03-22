from rest_framework import serializers
from .models import Session

from movies.serializers import MovieSerializer
 
 
class SessionSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
 
    class Meta:
        model  = Session
        fields = ('__all__')