from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import FollowUnfollowAPIView, followers_list, following_list
from .views import MessageListCreateView, ChatListView
urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

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
