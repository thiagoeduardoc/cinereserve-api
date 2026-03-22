from django.db import models
from movies.models import Movie


class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='sessions')
    room_name = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    room_capacity = models.PositiveIntegerField()

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.movie.title} - {self.room_name} - {self.start_time:%d/%m/%Y %H:%M}"


class Seat(models.Model):

    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Disponível'
        RESERVED = 'reserved',  'Reservado'
        PURCHASED = 'purchased', 'Comprado'

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=5)
    number = models.PositiveIntegerField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )

    class Meta:
        unique_together = ('session', 'row', 'number')
        ordering = ['row', 'number']

    def __str__(self):
        return f"{self.row}{self.number} [{self.get_status_display()}] - {self.session}"


class Ticket(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='tickets')
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE, related_name='ticket')
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-purchased_at']

    def __str__(self):
        return f"Ticket de {self.user.username} - {self.seat}"