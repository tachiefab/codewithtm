from django.utils.timesince import timesince
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse
from accounts.serializers import UserPublicSerializer
from comments.models import Comment
from comments.serializers import (
                                CommentSerializer, 
                                CommentListSerializer
                                )
from .models import Post
from likes.models import Like
from analytics.models import Analytic
from categories.serializers import CategorySerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    uri             = serializers.SerializerMethodField(read_only=True)
    date_display = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'uri',
            'id',
            'author',
            'image',
            'date_display',
            'timesince',
            'article',
        ]

    def get_image(self, obj):
        return obj.get_image_url()

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('api-posts:detail', kwargs={"slug": obj.slug}, request=request)

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"


class PostDetailInlineSerializer(PostSerializer):
    read_time = serializers.SerializerMethodField()
    category    = CategorySerializer(read_only=True)
    tags        = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()
    new_post = serializers.SerializerMethodField()
    older_post = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'uri',
            'id',
            'title',
            'slug',
            'category',
            'image',
            'read_time',
            'date_display',
            'timesince',
            'likes_count',
            'view_count',
            'did_like',
            'author',
            'comment_count',
            'tags',
            'article',
            'new_post',
            'older_post',
        ]

    def validate(self, data):
        article = data.get("article")
        if article == "":
            article = None
        image = data.get("image", None)
        if article is None:
            raise serializers.ValidationError("article is required.")
        return data

    def get_read_time(self, obj):
        read_time = obj.read_time
        return str(read_time) + " minutes read"

    def get_tags(self, obj):
        tags = obj.tags.all()
        track_tags = ", ".join([x.title for x in tags])
        return track_tags

    def get_likes_count(self, obj):
        sender = Post
        c_type = ContentType.objects.get_for_model(sender)
        likes = 0
        try:
            like_obj = Like.objects.get( content_type=c_type, object_id=obj.pk)
            likes = like_obj.likes_count
        except:
            pass
        return likes

    def get_did_like(self, obj):
        request = self.context.get("request")
        sender = Post
        c_type = ContentType.objects.get_for_model(sender)
        try:
            user = request.user
            if user.is_authenticated:
                try:
                    like_obj = Like.objects.get( content_type=c_type, object_id=obj.pk)
                    liked_users = like_obj.liked.all()
                except:
                    pass
                if user in liked_users:
                    return True
        except:
            pass
        return False

    def get_view_count(self, obj):
        sender = Post
        content_type = ContentType.objects.get_for_model(sender)
        post_qs = Analytic.objects.filter(content_type=content_type)
        post = post_qs.get(object_id=obj.id)
        return post.get_view_count

    def get_new_post(self, obj):
        return obj.get_next_url()

    def get_older_post(self, obj):
        return obj.get_previous_url()


class PostListInlineSerializer(PostSerializer):
    
    class Meta:
        model = Post
        fields = [
            'uri',
            'id',
            'title',
            'slug',
            'summary',
            'image',
            'date_display',
            'timesince',
            'author',
        ]

    def validate(self, data):
        article = data.get("article")
        if article == "":
            article = None
        image = data.get("image", None)
        if article is None:
            raise serializers.ValidationError("article is required.")
        return data


class PostListInlineMinimalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
        ]
