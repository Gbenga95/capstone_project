from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import RegisterView, welcome_view
from django.http import JsonResponse

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/logout/', lambda request: JsonResponse({"message": "Logged out"}, status=200), name='logout'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
]