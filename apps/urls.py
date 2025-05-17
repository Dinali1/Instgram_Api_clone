from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework.routers import DefaultRouter
from apps.views import *

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

from apps.views import RegisterView, ProfileView, ProfileUpdateView, PostViewSet

from apps.views import AllStoriesApiView, CreateStoriesApiView, GetUsersStoriesAPIView, ViewsUserAPIView

urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('profile/<username>/', ProfileView.as_view(), name='profile-detail'),

    path('profile/<username>/', ProfileUpdateView.as_view(), name='profile-update'),
    path('api/', include(router.urls)),

]

urlpatterns += [
    path('api/stories', AllStoriesApiView.as_view(), name='api_stories'),
    path('api/create/stories', CreateStoriesApiView.as_view(), name='api_create_stories'),
    path('api/stories/<int:pk>', GetUsersStoriesAPIView.as_view(), name='api_stories_pk'),
    path('view/stories/<int:pk>', ViewsUserAPIView.as_view(), name='api_stories_view'),
]
