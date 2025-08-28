from django.contrib import admin
from api.models import Genre, Movie, MovieGenre, Review, Rating

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(MovieGenre)
admin.site.register(Review)
admin.site.register(Rating)