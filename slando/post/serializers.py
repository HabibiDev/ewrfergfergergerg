from .models import Category, ImagePost, Post
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ImagePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImagePost
        fields = ('id', 'image_file', 'uploaded', 'post_image')



class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    images = ImagePostSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id',
                  'title',
                  'author',
                  'category',
                  'content',
                  'images',
                  'price',
                  'contract_price',
                  'created',
                  'updated',
                  'is_active'
                  )


class CategorySerializer(serializers.ModelSerializer):
    subcategories = RecursiveField(source="children",
                                   many=True, required=False)
    parent = serializers.ReadOnlyField(source='parent.name')

    class Meta:
        model = Category
        fields = ('id', 'parent', 'name', 'subcategories')
