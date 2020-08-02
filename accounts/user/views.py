from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, pagination
from rest_framework.response import Response
from accounts.permissions import AnonPermissionOnly
from posts.serializers import PostListInlineSerializer
from posts.views import PostAPIView
# from profiles.models import Followers, Friends
# from profiles.views import FollowersAPIView, FriendsAPIView
# from profiles.serializers import (
#                                 FollowersSerializer, 
#                                 FollowingsSerializer, 
#                                 FriendsSerializer
#                                 )
from posts.models import Post
from .serializers import UserDetailSerializer

User = get_user_model()

class UserDetailAPIView(generics.RetrieveAPIView):
    queryset            = User.objects.filter(is_active=True)
    serializer_class    = UserDetailSerializer
    lookup_field        = 'username'

    def get_serializer_context(self):
        return {'request': self.request}


class UserPostAPIView(PostAPIView):
    serializer_class            = PostListInlineSerializer
    
    def get_queryset(self, *args, **kwargs):
        username = self.kwargs.get("username", None)
        if username is None:
            return Post.objects.none()

        qs = Post.objects.filter(user__username=username).order_by("-timestamp")
        return qs

    def post(self, request, *args, **kwargs):
        return Response({"detail": "Not allowed here"}, status=400)


# class UserFollowersAPIView(FollowersAPIView):
#     serializer_class            = FollowersSerializer
    
#     def get_queryset(self, *args, **kwargs):
#         username = self.kwargs.get("username", None)
#         if username is None:
#             return Followers.objects.none()
#         follower_obj = get_object_or_404(Followers, user__username=username)
#         followers = follower_obj.followers.all()
#         return followers

# class UserFollowingsAPIView(FollowersAPIView):
#     serializer_class            = FollowingsSerializer
    
#     def get_queryset(self, *args, **kwargs):
#         username = self.kwargs.get("username", None)
#         if username is None:
#             return Followers.objects.none()
#         follower_obj = get_object_or_404(Followers, user__username=username)
#         followings = follower_obj.user.followings.all()
#         return followings

# class UserFriendsAPIView(FriendsAPIView):
#     serializer_class            = FriendsSerializer
    
#     def get_queryset(self, *args, **kwargs):
#         username = self.kwargs.get("username", None)
#         if username is None:
#             return Friends.objects.none()
#         friends_obj = get_object_or_404(Friends, user__username=username)
#         friends = friends_obj.friends.all()
#         return friends
#   