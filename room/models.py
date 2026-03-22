from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=50, unique=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} (Capacidade: {self.capacity})"


class Seat(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=5)
    seat_number = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('room', 'row', 'seat_number')
        ordering = ['row', 'seat_number']

    def __str__(self):
        return f"{self.room.name} - {self.row}{self.seat_number} ({'Disponível' if self.is_available else 'Indisponível'})"