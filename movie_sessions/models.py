from django.db import models
from django.utils import timezone
from datetime import timedelta
from movies.models import Movie
from room.models import Room, Seat


class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='sessions')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='sessions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.movie.title} - {self.room.name} - {self.start_time:%d/%m/%Y %H:%M}"


class Reservation(models.Model):
    """Reserva temporária de assento (lock de 10 minutos)"""
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='reservations')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='reservations')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='reservations')
    reserved_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        unique_together = ('seat', 'session')
        ordering = ['-reserved_at']

    def __str__(self):
        return f"Reserva de {self.user.username} - {self.seat} até {self.expires_at:%H:%M}"

    def is_valid(self):
        """Verifica se a reserva ainda está válida"""
        return timezone.now() < self.expires_at

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)


class Ticket(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='tickets')
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE, related_name='ticket')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='tickets')
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-purchased_at']

    def __str__(self):
        return f"Ticket de {self.user.username} - {self.seat}"