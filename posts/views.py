from rest_framework import generics, mixins, permissions
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from accounts.permissions import IsOwnerOrReadOnly
from .models import Post 
from categories.models import Category
from tags.models import Tag
from likes.models import Like
from analytics.models import Analytic
from .serializers import (
                        PostDetailInlineSerializer, 
                        PostListInlineSerializer, 
                        PostListInlineMinimalSerializer
                        )

class PostAPIDetailView(
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin, 
                    generics.RetrieveAPIView
                    ):

    permission_classes          = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class            = PostDetailInlineSerializer
    queryset                    = Post.objects.all()
    lookup_field                = 'slug'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        request = self.request
        instance = self.get_object()
        sender = Post
        c_type = ContentType.objects.get_for_model(sender)
        analytic_qs = Analytic.objects.get_or_create(
                    content_type=c_type,
                    object_id=instance.id
            )
        if analytic_qs:
            analytic_obj = analytic_qs[0]
            analytic_obj_view_count = analytic_obj.view_count
            total_view_count = analytic_obj_view_count + 1
            analytic_obj.view_count = total_view_count
            analytic_obj.save()
        qs = PostDetailInlineSerializer(instance, context={'request': request}).data
        return  Response(qs)


class PostAPIView(
                mixins.CreateModelMixin, 
                generics.ListAPIView
                ): 

    permission_classes          = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class            = PostListInlineSerializer
    passed_id                   = None
    search_fields               = ('user__username', 'article', 'user__email')
    ordering_fields             = ('user__username', 'timestamp')

    queryset                    = Post.objects.all()
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self, *args, **kwargs):
        queryset_list = []
        category_slug = self.request.GET.get("category")
        tag_slug = self.request.GET.get("tag")
        if category_slug:
            category_qs  = get_object_or_404(Category, slug=category_slug)
            queryset_list = Post.objects.filter(category=category_qs)
        elif tag_slug:
            tag_qs  = get_object_or_404(Tag, slug=tag_slug)
            queryset_list = Post.objects.filter(tags__title__icontains=tag_qs)
        else:
            queryset_list = Post.objects.all()
        return queryset_list


class RelatedPostAPIView(generics.ListAPIView):
    serializer_class = PostListInlineMinimalSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = []
        post_slug = self.request.GET.get("post_slug")
        if post_slug:
            post_qs  = get_object_or_404(Post, slug=post_slug)
            queryset_list = post_qs.category.post_set.all().exclude(slug=post_slug)
        else:
            queryset_list = Post.objects.all()[:5]
        return queryset_list




class LikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'

    def get(self, request, slug, format=None):
        sender = Post
        c_type = ContentType.objects.get_for_model(sender)
        try:
            post_obj = Post.objects.get(slug=slug)
            if post_obj:
                try:
                    pk = post_obj.id
                    like_qs = Like.objects.get(content_type=c_type, object_id=pk)
                except:
                    pass
                if like_qs:
                    if request.user.is_authenticated:
                        is_liked = Like.objects.like_toggle(request.user, sender, like_qs)
                        return Response({
                                        'liked': is_liked,
                                        'likes_count': like_qs.likes_count
                                        }
                                        )
        except:
            message = "Post does not exist"
        return Response({"message": message}, status=400)
