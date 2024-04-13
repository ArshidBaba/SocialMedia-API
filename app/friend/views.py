"""
Views for the Friends API.
"""

from rest_framework import viewsets
from rest_framework import generics, authentication, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import FriendRequest, User
from .serializers import FriendRequestSerializer, FriendRequestCreateSerializer


class FriendRequestViewSet(viewsets.ModelViewSet):
    """View for manage Friend request APIs."""

    serializer_class = FriendRequestCreateSerializer
    queryset = FriendRequest.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retrieve friend requests for authenticated users."""
        print(self.request.user.id)
        return self.queryset.filter(reciever=self.request.user.id)

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == "list":
            return FriendRequestSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new friend request"""
        serializer.save(sender=self.request.user)


# class ListFriendRequestAPIView(generics.ListCreateAPIView):
#     """List friend requests to authenticated user in the system."""

#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = FriendRequest.objects.all()
#     serializer_class = FriendRequestSerializer

#     # def perform_create(self, serializer):

#     #     return
#     def get_queryset(self):
#         friend_requests = FriendRequest.objects.values("id", "sender", "status").filter(
#             reciever=self.request.user
#         )
#         return friend_requests.all()

#     def list(self, request):
#         # Note the use of `get_queryset()` instead of `self.queryset`
#         queryset = self.get_queryset()
#         serializer = FriendRequestSerializer(queryset, many=True)
#         return Response(serializer.data)


# class CreateFriendRequestAPIView(generics.CreateAPIView):
#     """Create a new friend request in the system"""

#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     # queryset = FriendRequest.objects.all()
#     serializer_class = FriendRequestSerializer
