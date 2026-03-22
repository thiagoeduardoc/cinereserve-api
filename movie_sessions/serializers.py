from rest_framework import serializers
from .models import Session, Seat, Ticket


class SessionSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = Session
        fields = ('id', 'movie', 'movie_title', 'room_name', 'start_time', 'end_time', 'room_capacity')


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ('id', 'row', 'number', 'status')


class TicketSerializer(serializers.ModelSerializer):
    seat = SeatSerializer(read_only=True)
    session = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ('id', 'seat', 'session', 'purchased_at')

    def get_session(self, obj):
        return {
            'id': obj.seat.session.id,
            'movie': obj.seat.session.movie.title,
            'room': obj.seat.session.room_name,
            'start_time': obj.seat.session.start_time,
        }