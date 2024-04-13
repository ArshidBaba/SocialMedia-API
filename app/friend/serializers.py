"""
Serializers for the friends API View.
"""

from rest_framework import serializers

from core.models import FriendRequest, User


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

    # def get_sender(self, obj):
    #     """Get sender for the friend request"""
    #     print(obj)
    #     sender = User.objects.get(pk=self.request.user.id)
    #     return sender


# class FriendRequestSerializer(serializers.ModelSerializer):
#     """Serializer for the FriendRequest object."""

#     sender = serializers.SerializerMethodField(read_only=True)

#     # name = serializers.SerializerMethodField(read_only=True)
#     class Meta:
#         model = FriendRequest
#         fields = ["id", "sender", "status"]
#         extra_kwargs = {"password": {"write_only": True}}

#     def create(self, validated_data):
#         """Create and return a friend request."""
#         return FriendRequest.objects.create(**validated_data)

#     def get_sender(self, obj):
#         """To get the sender excluding the current user."""
#         sender = obj.sender.name
#         return sender


# class CreateFriendRequestSerializer(serializers.ModelSerializer):
#     """Serializer for creating a friend request."""

#     class Meta:
#         model = FriendRequest
#         fields = ["__all__"]

# def update(self, instance, validated_data):
#     """Update and return User."""
#     password = validated_data.pop("password", None)
#     user = super().update(instance, validated_data)

#     if password:
#         user.set_password(password)
#         user.save()

#     return user
