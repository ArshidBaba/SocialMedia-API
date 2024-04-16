"""
Views for the Friends API.
"""

from django.db import transaction
from django.db.models import Q


from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.serializers import ValidationError

from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import FriendRequest, Friend
from .serializers import (
    FriendRequestSerializer,
    FriendRequestCreateSerializer,
    FriendListSerializer,
    FriendCreateSerializer,
)
from .throttles import UserBasedCreateFriendRequestThrottle


class FriendRequestViewSet(viewsets.ModelViewSet):
    """View for manage Friend request APIs."""

    serializer_class = FriendRequestCreateSerializer
    queryset = FriendRequest.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = []

    def get_queryset(self):
        """Retrieve friend requests for authenticated users."""

        return self.queryset.filter(receiver=self.request.user.id)

    def get_serializer_class(self):
        """Return the serializer class for request."""

        if self.action == "list":
            return FriendRequestSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        """Create a new friend request"""

        receiver = int(request.data["receiver"])

        if receiver == int(request.user.id):
            raise ValidationError(
                {
                    "message": "The User cannot send a friend request to themself",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )
        f_request = FriendRequest.objects.filter(
            receiver=receiver, sender=request.user.id
        )

        if f_request:
            return Response(
                {
                    "message": "You have already sent a friend request to this user",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        f_request = FriendRequest.objects.filter(
            receiver=request.user.id, sender=receiver
        )
        if f_request:
            return Response(
                {
                    "message": "You already have a friend request from this user",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        friend = Friend.objects.filter(user1=request.user.id, user2=receiver)

        if friend:
            return Response(
                {
                    "message": "You are already friends with this user",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        throttle_instance = UserBasedCreateFriendRequestThrottle()

        if not throttle_instance.allow_request(request, self):
            return Response(
                {"message": "Rate limit exceeded. Try again after 1 minute."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {
                "message": "Friend request sent successfully!",
                "status": status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED,
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def destroy(self, request, pk=None):
        """Reject a friend request"""

        try:
            f_request = FriendRequest.objects.get(id=pk)
        except FriendRequest.DoesNotExist:
            return Response(
                {
                    "message": "The friend request with this ID does not exist.",
                    "status": status.HTTP_404_NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
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
def accept_friend_request(request):
    """Accepts a friend request from a user"""

    reciever = request.user

    try:
        f_request = FriendRequest.objects.get(pk=request.data["request_id"])
    except FriendRequest.DoesNotExist:
        return Response(
            {
                "message": "The friend request with this ID does not exist.",
                "status": status.HTTP_404_NOT_FOUND,
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    data = {"user1": f_request.sender.id, "user2": reciever.id}
    serializer = FriendCreateSerializer(data=data)
    if serializer.is_valid():
        serializer.save()

    data2 = {"user1": reciever.id, "user2": f_request.sender.id}
    serializer = FriendCreateSerializer(data=data2)
    if serializer.is_valid():
        serializer.save()
    f_request.delete()
    return Response(
        {
            "message": "Friend request accepted successfully!",
            "status": status.HTTP_200_OK,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def list_friends(request):
    """List all friends of an authenticated user"""

    authenticated_user = request.user.id

    friends_query = Friend.objects.filter(user1=authenticated_user)

    serializer = FriendListSerializer(friends_query, many=True)

    return Response(
        {"Friends": serializer.data, "status": status.HTTP_200_OK},
        status=status.HTTP_200_OK,
    )
