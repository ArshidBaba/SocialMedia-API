"""
URL mappings for the user API.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user import views


app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", views.ManageUserView.as_view(), name="me"),
    path("list/", views.list_users, name="list"),
    path("users/", views.UserList.as_view(), name="users"),
]
