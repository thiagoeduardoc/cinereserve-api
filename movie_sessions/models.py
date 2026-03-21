from django.db import models
from movies.models import Movie

class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='session')
    room_name = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    room_capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.movie} - {self.room_name} - {self.start_time}"