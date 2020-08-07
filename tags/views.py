import random
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, permissions 
from .serializers import TagSerializer
from .models import Tag
from posts.models import Post


class TagListAPIView(generics.ListAPIView): 
    permission_classes          = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class            = TagSerializer
    queryset 					=  Tag.objects.all()

    def get_queryset(self, *args, **kwargs):
        post_slug = self.request.GET.get("post_slug")
        tags = Tag.objects.all()[:10]
        if post_slug:
            post_qs  = get_object_or_404(Post, slug=post_slug)
            tags = post_qs.tags.all()
        return tags

    