from .models import Post, ImagePost, Category
from rest_framework import generics, renderers, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from django.contrib.auth.models import User
from .permissions import IsAuthorOrReadOnly
from django_filters import rest_framework as filters
import django_filters
from .serializers import (UserSerializer,
                          CategorySerializer,
                          ImagePostSerializer,
                          PostSerializer)


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          permissions.IsAdminUser)


class ImageFilter(filters.FilterSet):
    class Meta:
        model = ImagePost
        fields = ['post_image', ]


class ImagePostViewSet(viewsets.ModelViewSet):

    queryset = ImagePost.objects.all()
    serializer_class = ImagePostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ImageFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = Post.objects.get(id=request.data.get('post_image'))
        if post.author != request.user:
            raise PermissionDenied(
                "You can't add image to this post, you are't not author")
        elif len(post.images()) >= 8:
            raise PermissionDenied(
                "You can't save more than 8 pictures")
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class PostFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = filters.ModelChoiceFilter(
        queryset=Category.objects.all(), method='category_filter')

    class Meta:
        model = Post
        fields = ['category', 'min_price', 'max_price']

    def category_filter(self, queryset, name, value):
        queryset = value.posts()
        return queryset


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(is_active=True).order_by('-updated')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
