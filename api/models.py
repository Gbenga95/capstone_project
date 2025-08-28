from django.db import models
from django.contrib.auth.models import User
from enum import Enum

class Sentiment(Enum):
    POSITIVE = 'Positive'
    NEGATIVE = 'Negative'
    NEUTRAL = 'Neutral'

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_year = models.IntegerField()
    description = models.TextField(blank=True)
    poster_url = models.URLField(blank=True)
    genres = models.ManyToManyField(Genre, through='MovieGenre')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('movie', 'genre')

    def __str__(self):
        return f"{self.movie.title} - {self.genre.name}"

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    sentiment = models.CharField(max_length=10, choices=[(s.value, s.value) for s in Sentiment])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('movie', 'user')  # Ensures one rating per user per movie

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}: {self.stars}"