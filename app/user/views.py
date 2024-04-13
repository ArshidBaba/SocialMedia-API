"""
Views for the user API.
"""

from rest_framework import generics, authentication, permissions
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.views import SpectacularAPIView

from user.serializers import (
    UserSerializer,
    MyTokenObtainPairSerializer,
    UserListSerializer,
)
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


@api_view(["GET"])
def list_users(request):
    users = User.objects.all()
    serializer = UserListSerializer(users, many=True)

    return Response(serializer.data)


# class MySpectacularAPIView(SpectacularAPIView):
#     """Custom SpectacularAPIView."""

#     authentication_classes = []
