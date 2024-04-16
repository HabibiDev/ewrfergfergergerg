from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from rest_framework.reverse import reverse as api_reverse
from django.dispatch import receiver
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token


class Category(MPTTModel):
    name = models.CharField(max_length=80, unique=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def posts(self):
        return Post.objects.filter(category__in=Category.objects.get(id=self.id).
                                   get_descendants(include_self=True))

    def __str__(self):
        return self.name


def get_path(instance, filename):
    return '{0}/{1}/{2}'.format(instance.post_image.category,
                                instance.post_image.title,
                                filename)


class ImagePost(models.Model):
    image_file = models.ImageField(
        upload_to=get_path, null=True, blank=True, max_length=500)
    post_image = models.ForeignKey(
        'Post', on_delete=models.SET_NULL, null=True, blank=True, related_name='image_post')
    uploaded = models.DateTimeField(auto_now=True)


class Post(models.Model):
    title = models.CharField(max_length=100, unique=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    category = TreeForeignKey(
        Category, on_delete=models.CASCADE, related_name='posts_category')
    content = models.TextField(max_length=5000, null=True, blank=True)
    price = models.FloatField()
    contract_price = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def images(self):
        return ImagePost.objects.filter(post_image=self.id)

    def __str__(self):
        return self.title

    def get_api_url(self, request=None):
        return api_reverse('post:posts-detail', kwargs={'pk': self.pk}, request=request)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
