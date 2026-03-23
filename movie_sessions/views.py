from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Session, Ticket, Reservation
from .serializers import SessionSerializer, SeatSerializer, TicketSerializer, ReservationSerializer
from room.models import Seat


class SessionListView(generics.ListAPIView):
    serializer_class = SessionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Session.objects.filter(movie_id=self.kwargs['movie_id'])


class SeatListView(generics.ListAPIView):
    serializer_class = SeatSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        session = Session.objects.get(pk=self.kwargs['session_id'])
        self.request.session_instance = session
        return Seat.objects.filter(room=session.room)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['session'] = getattr(self.request, 'session_instance', None)
        return context


class ReserveView(generics.GenericAPIView):
    """Lock temporário (10 minutos) de um assento para reserva"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReservationSerializer

    def post(self, request, session_id, seat_id):
        try:
            session = Session.objects.get(pk=session_id)
        except Session.DoesNotExist:
            return Response({'error': 'Sessão não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            seat = Seat.objects.get(pk=seat_id, room=session.room)
        except Seat.DoesNotExist:
            return Response({'error': 'Assento não encontrado nesta sala.'}, status=status.HTTP_404_NOT_FOUND)

        if not seat.is_available:
            return Response({'error': 'Assento indisponível (fora de serviço).'}, status=status.HTTP_400_BAD_REQUEST)

        # Verifica se existe Ticket para este assento nesta sessão
        if Ticket.objects.filter(session=session, seat=seat).exists():
            return Response({'error': 'Assento já comprado para esta sessão.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verifica se existe Reservation não expirada
        reservation = Reservation.objects.filter(seat=seat, session=session).first()
        if reservation and reservation.is_valid():
            return Response({
                'error': 'Assento já reservado.',
                'reserved_by': reservation.user.username,
                'expires_at': reservation.expires_at
            }, status=status.HTTP_400_BAD_REQUEST)

        # Deleta Reservation expirada se existir
        if reservation:
            reservation.delete()

        # Cria nova Reservation (10 minutos)
        reservation = Reservation.objects.create(
            user=request.user,
            seat=seat,
            session=session
        )

        return Response(
            ReservationSerializer(reservation).data,
            status=status.HTTP_201_CREATED
        )


class PurchaseView(generics.GenericAPIView):
    """Converte Reservation em Ticket (finaliza compra)"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketSerializer

    def post(self, request, session_id, seat_id):
        try:
            session = Session.objects.get(pk=session_id)
        except Session.DoesNotExist:
            return Response({'error': 'Sessão não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            seat = Seat.objects.get(pk=seat_id, room=session.room)
        except Seat.DoesNotExist:
            return Response({'error': 'Assento não encontrado nesta sala.'}, status=status.HTTP_404_NOT_FOUND)

        # Valida Reservation
        try:
            reservation = Reservation.objects.get(seat=seat, session=session, user=request.user)
        except Reservation.DoesNotExist:
            return Response({
                'error': 'Nenhuma reserva ativa encontrada. Faça uma reserva antes de comprar.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not reservation.is_valid():
            return Response({
                'error': 'Reserva expirada. Faça uma nova reserva.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verifica se não foi comprado enquanto esperava
        if Ticket.objects.filter(session=session, seat=seat).exists():
            reservation.delete()
            return Response({
                'error': 'Assento foi vendido para outro usuário. Reserva cancelada.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Cria Ticket e deleta Reservation
        ticket = Ticket.objects.create(
            user=request.user,
            seat=seat,
            session=session
        )
        reservation.delete()

        return Response(
            TicketSerializer(ticket).data,
            status=status.HTTP_201_CREATED
        )


class MyReservationsView(generics.ListAPIView):
    """Lista reservas ativas do usuário (que ainda não expirou)"""
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user, expires_at__gt=timezone.now())


class MyTicketsView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

