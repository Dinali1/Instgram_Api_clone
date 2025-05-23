from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework.routers import DefaultRouter
from apps.views import *

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from apps.views import NotificationListView, TagsListView, NotificationViewSet


from apps.views import RegisterView, ProfileView, ProfileUpdateView, PostViewSet

from apps.views import AllStoriesApiView, CreateStoriesApiView, GetUsersStoriesAPIView, ViewsUserAPIView

from .views import FollowUnfollowAPIView, followers_list, following_list
from .views import MessageListCreateView, ChatListView
urlpatterns = [
    path('user/notification', NotificationListView.as_view(), name='get_notification'),
    path('user/notification/<int:id>/read', NotificationViewSet.as_view(), name='notification-list'),
    path('tags-list/<str:tag>/posts/', TagsListView.as_view(), name='tags-list'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
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

# Mirahmad
urlpatterns += [
    path('api/follow/<str:username>/', FollowUnfollowAPIView.as_view(), name='follow'),
    path('api/<str:username>/followers/', followers_list, name='followers_list'),
    path('api/<str:username>/following/', following_list, name='following_list'),
]


urlpatterns += [
    path('api/messages/<str:username>/', MessageListCreateView.as_view(), name='message_list_create'),
    path('api/chats/', ChatListView.as_view(), name='chat_list'),
]
