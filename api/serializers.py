from rest_framework import serializers
from api.models import Movie, Genre, Review, Rating, MovieGenre
from textblob import TextBlob
from django.db.models import Avg

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class MovieGenreSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()

    class Meta:
        model = MovieGenre
        fields = ['genre']

class MovieSerializer(serializers.ModelSerializer):
    genres = MovieGenreSerializer(source='moviegenre_set', many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'release_year', 'description', 'poster_url', 'genres', 'average_rating', 'created_at']

    def get_average_rating(self, obj):
        avg = obj.ratings.aggregate(Avg('stars'))['stars__avg']
        return round(avg, 2) if avg else 0

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    sentiment = serializers.CharField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'movie', 'user', 'review_text', 'sentiment', 'created_at']

    def create(self, validated_data):
        review_text = validated_data['review_text']
        blob = TextBlob(review_text)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            sentiment = 'Positive'
        elif polarity < 0:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        validated_data['sentiment'] = sentiment
        validated_data['user'] = self.context['request'].user
        return Review.objects.create(**validated_data)

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'movie', 'user', 'stars', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Rating.objects.create(**validated_data)