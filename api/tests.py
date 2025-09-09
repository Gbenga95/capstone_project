from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Movie, Genre, Review, Rating
from api.serializers import MovieSerializer, ReviewSerializer
from textblob import TextBlob
import json

class MovieModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.genre = Genre.objects.create(name="Action")
        self.movie = Movie.objects.create(title="Test Movie", release_year=2023)
        self.movie.genres.add(self.genre)
        self.rating = Rating.objects.create(movie=self.movie, user=self.user, stars=5)
        self.review = Review.objects.create(movie=self.movie, user=self.user, review_text="Great film!")

    def test_movie_creation(self):
        self.assertEqual(self.movie.title, "Test Movie")
        self.assertEqual(self.movie.release_year, 2023)
        self.assertIn(self.genre, self.movie.genres.all())

    def test_rating_creation(self):
        self.assertEqual(self.rating.stars, 5)
        self.assertEqual(self.rating.movie, self.movie)
        self.assertEqual(self.rating.user, self.user)

    def test_review_creation(self):
        self.assertEqual(self.review.review_text, "Great film!")
        self.assertEqual(self.review.sentiment, "Positive")

class MovieSerializerTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Comedy")
        self.movie = Movie.objects.create(title="Funny Movie", release_year=2022)
        self.movie.genres.add(self.genre)
        self.serializer = MovieSerializer(instance=self.movie)

    def test_movie_serializer(self):
        data = self.serializer.data
        self.assertEqual(data["title"], "Funny Movie")
        self.assertEqual(data["release_year"], 2022)
        self.assertIn("Comedy", [g.get("name") for g in data["genres"]])

class APITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.admin = User.objects.create_user(
            username="adminuser", password="adminpass123", is_staff=True
        )
        self.genre = Genre.objects.create(name="Action")
        self.movie = Movie.objects.create(title="Test Movie", release_year=2023)
        self.movie.genres.add(self.genre)
        self.user_token = self.get_token("testuser", "testpass123")
        self.admin_token = self.get_token("adminuser", "adminpass123")

    def get_token(self, username, password):
        response = self.client.post(
            "/api/auth/login/",
            {"username": username, "password": password},
            format="json",
        )
        return response.data["access"]

    def test_register_endpoint(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "newpass123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_endpoint(self):
        response = self.client.post(
            "/api/auth/login/",
            {"username": "testuser", "password": "testpass123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_list_movies_unauthenticated(self):
        response = self.client.get("/api/movies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_movie_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.post(
            "/api/movies/",
            {
                "title": "New Movie",
                "release_year": 2024,
                "description": "A great film",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Movie")

    def test_create_movie_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.post(
            "/api/movies/",
            {
                "title": "Unauthorized Movie",
                "release_year": 2024,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_review_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.post(
        "/api/reviews/",
        {"movie": self.movie.id, "review_text": "Amazing film!"},
        format="json",
    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["review_text"], "Amazing film!")
        self.assertEqual(response.data["sentiment"], "Positive")

    def test_filter_reviews_by_sentiment(self):
        Review.objects.create(movie=self.movie, user=self.user, review_text="Great film!")
        response = self.client.get("/api/reviews/?sentiment=Positive")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        for review in response.data:
            self.assertEqual(review.get("sentiment"), "Positive")

    def test_movie_average_rating(self):
        Rating.objects.create(movie=self.movie, user=self.user, stars=5)
        response = self.client.get(f"/api/movies/{self.movie.id}/average-rating/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data["average_rating"]), 5.0)

    def test_movie_ratings(self):
        Rating.objects.create(movie=self.movie, user=self.user, stars=4)
        response = self.client.get(f"/api/ratings/movie/{self.movie.id}/ratings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["stars"], 4)

        