"""
Views for the Friends API.
"""

from django.db import transaction
from django.db.models import Q

from rest_framework import viewsets
from rest_framework import generics, authentication, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.serializers import ValidationError

from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import FriendRequest, User, Friend
from .serializers import (
    FriendRequestSerializer,
    FriendRequestCreateSerializer,
    FriendSerializer,
)


class FriendRequestViewSet(viewsets.ModelViewSet):
    """View for manage Friend request APIs."""

    serializer_class = FriendRequestCreateSerializer
    queryset = FriendRequest.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retrieve friend requests for authenticated users."""

        return self.queryset.filter(reciever=self.request.user.id)

    def get_serializer_class(self):
        """Return the serializer class for request."""

        if self.action == "list":
            return FriendRequestSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new friend request"""

        reciever = self.request.data["reciever"]
        print(reciever)
        print(self.request.user.id)
        if reciever == self.request.user.id:
            raise ValidationError(
                {"message": "The User cannot send a friend request to themself"}
            )
        serializer.save(sender=self.request.user)

    def destroy(self, request, pk=None):
        """Reject a friend request"""

        print("Inside Destroy")
        try:
            f_request = FriendRequest.objects.get(id=pk)
        except:
            raise Not
        f_request.delete()
        return Response(
            {
                "message": "Friend Request rejected successfully!",
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
@transaction.atomic
def accept_friend_request(request, pk):
    """Accepts a friend request from a user"""

    reciever = request.user
    f_request = FriendRequest.objects.get(pk=pk)

    data = {"user1": f_request.sender.id, "user2": reciever.id}
    serializer = FriendSerializer(data=data)
    if serializer.is_valid():
        serializer.save()

    data2 = {"user1": reciever.id, "user2": f_request.sender.id}
    serializer = FriendSerializer(data=data2)
    if serializer.is_valid():
        serializer.save()
    f_request.delete()
    return Response("Finish")


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def list_friends(request):
    """List all friends of an authenticated user"""

    authenticated_user = request.user.id

    friends_query = Friend.objects.filter(user1=authenticated_user)

    serializer = FriendSerializer(friends_query, many=True)

    return Response(serializer.data)
