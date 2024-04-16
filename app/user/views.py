"""
Views for the user API.
"""

from rest_framework import filters
from rest_framework import generics, authentication, permissions
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.views import SpectacularAPIView

from user.serializers import (
    UserSerializer,
    MyTokenObtainPairSerializer,
    UserListSerializer,
)
from core.models import User
from .pagination import MyPageNumberPagination


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    authentication_classes = []


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    authentication_classes = []
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class UserList(generics.ListAPIView):
    """User list in the system."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "email"]
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        """Retrieve and return list of users."""

        users = self.queryset.all()
        return users
