"""
Serializers for the friends API View.
"""

from rest_framework import serializers

from core.models import FriendRequest, User, Friend


class FriendRequestSerializer(serializers.ModelSerializer):
    """Serializer for the FriendRequest object."""

    sender = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ["id", "sender", "status"]
        read_only_fields = ["id"]
        # write_only_fields = ["reciever"]

    def get_sender(self, obj):
        """To get the sender excluding the current user."""
        sender = obj.sender.name
        return sender


class FriendRequestCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating friend request object."""

    class Meta:
        model = FriendRequest
        fields = ["sender", "reciever", "status"]
        extra_kwargs = {
            "sender": {"write_only": True},
            "reciever": {"write_only": True},
        }


class FriendSerializer(serializers.ModelSerializer):
    """Serializer for creating a friend."""

    user2 = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Friend
        fields = ["id", "user2"]

    def get_user2(self, obj):
        """Method to get the name of the user2"""
        name = obj.user2.name
        return name
