from rest_framework import serializers
from django.utils import timezone
from .models import Session, Ticket, Reservation
from room.models import Seat


class SessionSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)

    class Meta:
        model = Session
        fields = ('id', 'movie', 'movie_title', 'room', 'room_name', 'start_time', 'end_time')


class SeatSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = ('id', 'row', 'seat_number', 'is_available', 'status')

    def get_status(self, obj):
        """
        Status: 'available', 'reserved' (lock 10min), 'purchased', 'unavailable'
        """
        session = self.context.get('session')
        
        if not obj.is_available:
            return 'unavailable'
        
        # Verifica se tem Reservation válida para esta sessão
        if session:
            reservation = Reservation.objects.filter(seat=obj, session=session).first()
            if reservation and reservation.is_valid():
                return 'reserved'
            
            # Verifica se tem Ticket para esta sessão
            if Ticket.objects.filter(session=session, seat=obj).exists():
                return 'purchased'
        
        return 'available'


class ReservationSerializer(serializers.ModelSerializer):
    seat_row = serializers.CharField(source='seat.row', read_only=True)
    seat_number = serializers.IntegerField(source='seat.seat_number', read_only=True)
    movie_title = serializers.CharField(source='session.movie.title', read_only=True)
    room_name = serializers.CharField(source='session.room.name', read_only=True)
    time_remaining = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ('id', 'seat_row', 'seat_number', 'movie_title', 'room_name', 
                  'reserved_at', 'expires_at', 'time_remaining')
        read_only_fields = ('reserved_at', 'expires_at')

    def get_time_remaining(self, obj):
        """Tempo restante em segundos"""
        if obj.is_valid():
            delta = obj.expires_at - timezone.now()
            return int(delta.total_seconds())
        return 0


class TicketSerializer(serializers.ModelSerializer):
    seat = SeatSerializer(read_only=True)
    session = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ('id', 'seat', 'session', 'purchased_at')

    def get_session(self, obj):
        return {
            'id': obj.session.id,
            'movie': obj.session.movie.title,
            'room': obj.session.room.name,
            'start_time': obj.session.start_time,
        }
