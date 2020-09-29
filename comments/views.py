from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
    )
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    )
from accounts.permissions import IsOwnerOrReadOnly
from comments.models import Comment
from posts.models import Post
from .serializers import (
    CommentListSerializer,
    CommentDetailSerializer,
    CommentCreateSerializer
    )
from likes.models import Like

User = get_user_model()

class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super(CommentCreateAPIView, self).get_serializer_context()
        user = None
        if self.request.user.is_authenticated:
            user = self.request.user
        context['user'] = user
        return context


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommentListAPIView(ListAPIView):
    serializer_class = CommentDetailSerializer
    permission_classes = [AllowAny]
    search_fields = ['content', 'user__first_name']

    def get_queryset(self, *args, **kwargs):
        queryset_list = []
        query = self.request.GET.get("q")
        obj_slug = self.request.GET.get("slug")
        if obj_slug:
            obj_qs          = Post.objects.filter(slug=obj_slug)#Modified to go for content types 
            if obj_qs.exists():
                content_obj     = obj_qs.first()
                queryset_list   = Comment.objects.filter_by_instance(content_obj)
        else:
            queryset_list = Comment.objects.filter(id__gte=0)
        if query:
            queryset_list = queryset_list.filter(
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
                    ).distinct()
        return queryset_list

class CommentLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk, format=None):
        sender = Comment
        c_type = ContentType.objects.get_for_model(sender)
        try:
            comment_obj = Comment.objects.get(id=pk)
            if comment_obj:
                try:
                    pk = comment_obj.id
                    like_qs = Like.objects.get(content_type=c_type, object_id=pk)
                except:
                    pass
                if like_qs:
                    if request.user.is_authenticated:
                        is_liked = Like.objects.like_toggle(request.user, sender, like_qs)
                        print(request.user)
                return Response({
                                'liked': is_liked,
                                'likes_count': like_qs.likes_count
                                }
                                )
        except:
            message = "Comment does not exist"
            return Response({"message": message}, status=400)


