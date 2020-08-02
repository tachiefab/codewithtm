from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, permissions, pagination
from analytics.models import Analytic
from posts.models import Post
from posts.serializers import PostListInlineSerializer



class MostViewedPostListAPIView(generics.ListAPIView):
    serializer_class = PostListInlineSerializer

    def get_queryset(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(Post)
        try:
            post_posts = Analytic.objects.filter(content_type=content_type)
            most_viewed_posts = [x.content_object for x in post_posts]
            top_viewed_post = Post.objects.filter(title__in=most_viewed_posts)
        except:
            top_viewed_post = None
        return top_viewed_post[:6]
