from django.shortcuts import render
from django.http import JsonResponse  # Added for welcome_view
from rest_framework import viewsets, permissions, generics, status, serializers
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.db.models import Avg
from .models import Movie, Genre, Review, Rating
from .serializers import MovieSerializer, GenreSerializer, ReviewSerializer, RatingSerializer

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by('id')
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    @action(detail=True, methods=['get'], url_path='average-rating')
    def average_rating(self, request, pk=None):
        movie = self.get_object()
        ratings = Rating.objects.filter(movie=movie)
        avg_rating = ratings.aggregate(Avg('stars'))['stars__avg'] or 0.0
        return Response({'average_rating': avg_rating}, status=status.HTTP_200_OK)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('id')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sentiment']

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all().order_by('id')
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path=r'movie/(?P<movie_id>\d+)/ratings')
    def movie_ratings(self, request, movie_id=None):
        ratings = Rating.objects.filter(movie_id=movie_id)
        serializer = self.get_serializer(ratings, many=True)
        return Response(serializer.data)

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def welcome_view(request):
    return JsonResponse({
        'message': 'Welcome to the Movie Review & Rating API! Access endpoints at /api/ or authenticate at /api/auth/.'
    })