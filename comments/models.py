from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from codewithtm.validators import validate_content
# from likes.tasks import auto_create_likes


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id= obj_id).filter(parent=None)
        return qs

    def create_by_model_type(self, model_type, slug, content, name, email, website, user, parent_obj=None):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=slug)
            # obj_qs = SomeModel.objects.filter(id=obj_id) 
            #use this when comments are created based on id
            if obj_qs.exists() and obj_qs.count() == 1:
                instance = self.model()
                instance.content = content
                instance.name = name
                instance.email = email
                instance.website = website
                instance.user = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                if parent_obj:
                    instance.parent = parent_obj
                instance.save()
                return instance
        return None


class Comment(models.Model):
    user  = models.ForeignKey(
                settings.AUTH_USER_MODEL,
                null=True, 
                blank=True,
                on_delete=models.CASCADE, 
                related_name='user_comments'
                )
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=220, null=True, blank=True)
    website = models.CharField(max_length=220, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent      = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField(validators=[validate_content])
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.content)

    # def get_absolute_url(self):
    #     return reverse("comments:thread", kwargs={"id": self.id})

    # def get_delete_url(self):
    #     return reverse("comments:delete", kwargs={"id": self.id})

    def children(self): #replies
        return Comment.objects.filter(parent=self)

    @property
    def owner(self):
        return self.user
    

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True


def comment_like_receiver(sender, instance, created, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    if created:
        pass
        # auto_create_likes.delay(instance.id, 'comment')
        # new_like_obj = Like.objects.create(
        #             content_type=c_type,
        #             object_id=instance.id
        #     )

post_save.connect(comment_like_receiver, sender=Comment)