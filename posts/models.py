import re
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
# from tags.signals import parsed_tags
from codewithtm.validators import validate_content
from codewithtm.utils import unique_slug_generator
from authors.models import Author
from likes.models import Like
from tags.models import Tag
from categories.models import Category
from comments.models import Comment
from notifications.tasks import notifications, add
from .choices import STATUSES, STATUS_PUBLISHED
from .utils import get_read_time, get_post_for_direction

User = get_user_model()


class PostManager(models.Manager):
    def all(self, *args, **kwargs):
        return super(PostManager, self).filter(status=STATUS_PUBLISHED).filter(published_date__lte=timezone.now())

class Post(models.Model):
    author = models.ForeignKey(
        Author,
        related_name="author_posts",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=90)
    slug = models.SlugField(max_length=90, unique=True)
    image_path = models.TextField(blank=True, null=True)
    article = models.TextField(validators=[validate_content])
    summary = models.TextField(validators=[validate_content])
    read_time =  models.IntegerField(default=0)
    category = models.ForeignKey(
                            Category,  
                            on_delete=models.CASCADE,
                            blank=True,
                            null=True
                            )
    order = models.PositiveIntegerField(default=1)
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(max_length=20, choices=STATUSES)
    published_date = models.DateField(auto_now=False, auto_now_add=False)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = PostManager()

    def __str__(self):
        return str(self.title)


    class Meta:
        unique_together = ('slug', 'category')
        ordering = ['order', '-timestamp']

    @property
    def owner(self):
        return self.author

    def get_absolute_url(self):
        return reverse("api-posts:detail", kwargs={"slug":self.slug})

    def get_image_url(self):
        img = self.image_path
        if img:
            return img
        img = "https://static.staah.net/images/noimage-640x480.jpg"
        return img

    def get_next_url(self):
        post = get_post_for_direction(self, "next")
        if post is not None:
            return post.slug
        return None

    def get_previous_url(self):
        post = get_post_for_direction(self, "previous")
        if post is not None:
            return post.slug
        return None

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def comment_count(self):
        comment_total = self.comments.count()
        return comment_total



def post_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    if instance.article:
        article_string = instance.article
        read_time_var = get_read_time(article_string)
        instance.read_time = read_time_var

pre_save.connect(post_pre_save_receiver, sender=Post)


def post_like_receiver(sender, instance, created, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    if created:
        '''updating post order to have equal value as the it'''
        instance.order = instance.id
        instance.save()
        '''saving post like instance'''
        new_like_obj = Like.objects.create(
                    content_type=c_type,
                    object_id=instance.id
            )

    ''' Notifying users of a new post '''
    target_id = instance.id
    # username = logged_in_user.username
    # username = 'tachiefab'
    user = get_object_or_404(User, username='tachiefab')
    username = user.username
    verb = 'created a new post called '
    sender = Post
    content_type_id = ContentType.objects.get_for_model(Post).id
    # content_type = ContentType.objects.get_for_model(model=content_type_id)
    # print("Hi Tachie You are Genuis")
    # print(content_type_id)
    # print("Hi Tachie You are Genuis")
    # print(dir(content_type_id))
    # notifications.delay(username, target_id, content_type_id, verb)
    add.delay(10,10)

post_save.connect(post_like_receiver, sender=Post)

