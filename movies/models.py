from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=50)
    synopsis = models.TextField(max_length=300)
    genre = models.CharField(max_length=30)
    duration = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    