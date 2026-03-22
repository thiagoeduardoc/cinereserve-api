from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    synopsis = models.TextField()
    duration = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    GENRE_CHOICES = [
    ('action', 'Ação'),
    ('comedy', 'Comédia'),
    ('drama', 'Drama'),
    ('horror', 'Terror'),
    ('sci_fi', 'Ficção Científica'),
    ]
    
    genre = models.CharField(max_length=30, choices=GENRE_CHOICES)

    def __str__(self):
        return self.title
    