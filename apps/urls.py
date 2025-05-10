from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework.routers import DefaultRouter
from apps.views import  PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

from apps.views import RegisterView, ProfileView, ProfileUpdateView

urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('profile/<username>/', ProfileView.as_view(), name='profile-detail'),

    path('profile/<username>/', ProfileUpdateView.as_view(), name='profile-update'),
    path('api/', include(router.urls)),

]