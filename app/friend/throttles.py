from rest_framework.throttling import UserRateThrottle


class CreateFriendRequestThrottle(UserRateThrottle):
    scope = "create_friend_request"

    def get_rate(self):
        return "3/minute"
