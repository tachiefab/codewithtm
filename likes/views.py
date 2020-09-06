from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from posts.models import Post
from posts.serializers import PostListInlineSerializer
from likes.models import Like

User = get_user_model()


class LikedItemsListAPIView(ListAPIView):
    serializer_class = PostListInlineSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = []
        username = self.request.GET.get("username")
        type = self.request.GET.get("type", "post")
        if username:
            user = get_object_or_404(User, username=username)
            model_type      = type
            model_qs        = ContentType.objects.filter(model=model_type)
            if model_qs.exists():  
                SomeModel       = model_qs.first().model_class()
                like_qs   = Like.objects.filter(content_type=model_qs.first())
                for like in like_qs:
                    if user in like.liked.all():
                        obj_qs          = SomeModel.objects.filter(id=like.object_id)
                        print(obj_qs)
                        if obj_qs.exists():

                            content_obj     = obj_qs.first()
                            queryset_list.append(content_obj)
        return queryset_list