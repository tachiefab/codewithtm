from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.reverse import reverse as api_reverse
from django.utils.timesince import timesince
from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.serializers import UserPublicSerializer
from comments.models import Comment
from profiles.models import Profile
from likes.models import Like

User = get_user_model()
HOST_SERVER = settings.HOST_SERVER

class CommentSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    uri             = serializers.SerializerMethodField(read_only=True)


    user_profile_image = serializers.SerializerMethodField()
    comment_user_name = serializers.SerializerMethodField()
    # user_id = serializers.SerializerMethodField()


    date_display = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'uri',
            'content_type',
            'object_id',
            'parent',
            'content',
            'reply_count',
            'timesince',
            'date_display',
            'user',


            'comment_user_name',
            'user_profile_image'
        ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("comments-api:thread", kwargs={"pk": obj.pk}, request=request)

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d, %Y")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"

    def get_comment_user_name(self, obj):
        try:
            user = obj.user
            try:
                first_name = user.first_name
                last_name = user.last_name
                name = first_name + " " + last_name
            except:
                name = user.username
        except:
           name = obj.name
        return name

    def get_user_profile_image(self, obj):
        image = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'
        return image


class CommentCreateSerializer(CommentSerializer):
        # user = UserPublicSerializer(read_only=True)
        type = serializers.CharField(required=False, write_only=True)
        slug = serializers.CharField(required=True, write_only=True)
        parent_id = serializers.IntegerField(required=False)

        class Meta:
            model = Comment
            fields = [
                'id',
                'user',
                'name',
                'email',
                'website',
                'content',
                'type',
                'slug',
                'parent_id',
                'date_display',
                'timesince'
            ]

        def validate(self, data):
            model_type      = data.get("type", "post")
            model_qs        = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise serializers.ValidationError("This is not a valid content type")
            SomeModel       = model_qs.first().model_class()
            slug            = data.get("slug")
            obj_qs          = SomeModel.objects.filter(slug=slug)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise serializers.ValidationError("This is not a id for this content type")
            parent_id       = data.get("parent_id")
            if parent_id:
                parent_qs   = Comment.objects.filter(id=parent_id)
                if not parent_qs.exists() or parent_qs.count() !=1:
                    raise serializers.ValidationError("This is not a valid parent for this content")
            return data

        def create(self, validated_data):
            content         = validated_data.get("content")
            name         = validated_data.get("name")
            email         = validated_data.get("email")
            website         = validated_data.get("website")
            model_type      = validated_data.get("type", "post")
            slug            = validated_data.get("slug")
            parent_obj      = None
            parent_id       = validated_data.get("parent_id")
            if parent_id:
                parent_obj  = Comment.objects.filter(id=parent_id).first()
            user            = self.context['user']
            comment         = Comment.objects.create_by_model_type(
                                                                model_type, 
                                                                slug, 
                                                                content, 
                                                                name,
                                                                email,
                                                                website,
                                                                user,
                                                                parent_obj=parent_obj,
                                                            )
            return comment


class CommentListSerializer(CommentSerializer):
    reply_count = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'uri',
            'id',
            'content',
            'reply_count',
            'timesince',
            'date_display',
            'comment_user_name',
            'user_profile_image',
            # 'user',

        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentChildSerializer(CommentSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            # 'user',
            'content',
            'timesince',
            'date_display',
            'comment_user_name',
            'user_profile_image',
        ]
    read_only_fields = [
            'timesince',
            'date_display',
        ]

class CommentDetailSerializer(CommentSerializer):
    reply_count = serializers.SerializerMethodField()
    content_object_url = serializers.SerializerMethodField()
    replies =   serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'reply_count',
            'did_like',
            'likes_count',
            'timesince',
            'date_display',
            'content_object_url',
            # 'user',
            'comment_user_name',
            'user_profile_image',
            'replies',
        ]
        read_only_fields = [
            'reply_count',
            'replies',
        ]

    def get_content_object_url(self, obj):
        try:
            uri = obj.content_object.get_absolute_url()
            return HOST_SERVER + uri
        except:
            return None

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


    def get_did_like(self, obj):
        request = self.context.get("request")
        sender = Comment
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

    def get_likes_count(self, obj):
        sender = Comment
        c_type = ContentType.objects.get_for_model(sender)
        likes = 0
        try:
            like_obj = Like.objects.get( content_type=c_type, object_id=obj.pk)
            likes = like_obj.likes_count
        except:
            pass
        return likes
