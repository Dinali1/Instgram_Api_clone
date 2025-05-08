from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from apps.views import NotificationListView, TagsListView, NotificationMarkReadView

urlpatterns = [
    path('user/notification', NotificationListView.as_view(), name='notification-list'),
    path('user/notification/<int:id>/read', NotificationMarkReadView.as_view(), name='notification-list'),
    path('tags-list/<str:tag>/posts/', TagsListView.as_view(), name='tags-list'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
