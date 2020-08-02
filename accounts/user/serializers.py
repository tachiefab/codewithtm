import datetime
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.serializers import SerializerMethodField, ModelSerializer
from rest_framework.reverse import reverse as api_reverse
from posts.serializers import PostListInlineSerializer
from posts.models import Post
from profiles.serializers import PublicProfileSerializer

User = get_user_model()


class UserDetailSerializer(ModelSerializer):
    profile = PublicProfileSerializer(read_only=True)
    uri             = SerializerMethodField(read_only=True)
    posts          = SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'uri',
            'profile',
            'posts',
        ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("api-user:detail", kwargs={"username": obj.username}, request=request)

    def get_posts(self, obj):
        request = self.context.get('request')
        limit = 10
        if request:
            limit_query = request.GET.get('posts_limit')
            try:
                limit = int(limit_query)
            except:
                pass
        qs1 = obj.post_set.all().order_by("-timestamp")
        user_following = obj.followings.all()
        followings = user_following.exclude(user=obj)
        users = []
        for following in followings:
            user = get_object_or_404(User, username=following.user.username)
            users.append(user)
        qs2 = Post.objects.filter(user__in=users)
        qs = (qs1 | qs2).distinct().order_by("-timestamp")
        data = {
            'total': obj.post_set.all().count(),
            'uri': self.get_uri(obj) + "posts/",
            'last': PostListInlineSerializer(qs.first(), context={'request': request}).data,
            'recent': PostListInlineSerializer(qs[:limit], many=True, context={'request': request}).data
        }
        return data

   