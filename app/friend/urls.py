"""
URL mappings for the user API.
"""

from django.urls import path, include

from friend import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("requests", views.FriendRequestViewSet)
app_name = "friend"


urlpatterns = [
    path("", include(router.urls)),
    # path("requests/", views.ListFriendRequestAPIView.as_view(), name="list"),
    # path("request/", views.CreateFriendRequestAPIView.as_view(), name="create"),
]
