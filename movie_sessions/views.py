from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Session, Seat, Ticket
from .serializers import SessionSerializer, SeatSerializer, TicketSerializer


class SessionListView(generics.ListAPIView):
    serializer_class   = SessionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Session.objects.filter(movie_id=self.kwargs['movie_id'])


class SeatListView(generics.ListAPIView):
    serializer_class   = SeatSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Seat.objects.filter(session_id=self.kwargs['session_id'])


class ReserveView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id, seat_id):
        try:
            seat = Seat.objects.get(id=seat_id, session_id=session_id)
        except Seat.DoesNotExist:
            return Response({'error': 'Assento não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if seat.status != Seat.Status.AVAILABLE:
            return Response({'error': 'Assento não disponível.'}, status=status.HTTP_400_BAD_REQUEST)

        seat.status = Seat.Status.PURCHASED
        seat.save()

        ticket = Ticket.objects.create(user=request.user, seat=seat)
        return Response(TicketSerializer(ticket).data, status=status.HTTP_201_CREATED)


class MyTicketsView(generics.ListAPIView):
    serializer_class   = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)