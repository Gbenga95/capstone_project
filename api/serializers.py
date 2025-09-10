from rest_framework import serializers
from django.db.models import Avg
from .models import Movie, Genre, Review, Rating

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = ['id', 'title', 'release_year', 'description', 'genres', 'average_rating', 'created_at']
    def get_average_rating(self, obj):
        avg = obj.ratings.aggregate(Avg('stars'))['stars__avg']
        return round(avg, 2) if avg else 0

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'movie', 'review_text', 'sentiment', 'created_at']
        read_only_fields = ['user', 'sentiment', 'created_at']
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'movie', 'stars', 'created_at']
        read_only_fields = ['user']
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)