"""
Views for the user API.
"""

from rest_framework import generics, authentication, permissions
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.views import SpectacularAPIView

from user.serializers import UserSerializer, MyTokenObtainPairSerializer
from core.models import User


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    authentication_classes = []


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    authentication_classes = []
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


# class MySpectacularAPIView(SpectacularAPIView):
#     """Custom SpectacularAPIView."""

#     authentication_classes = []
