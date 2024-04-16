from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (PostViewSet,
                    ImagePostViewSet,
                    CategoryListView,
                    UserCreate)

app_name = 'post'

router = DefaultRouter()
router.register('posts', PostViewSet, 'posts')
router.register('images', ImagePostViewSet, 'images')


urlpatterns = [
    path('categories', CategoryListView.as_view(), name='categories'),
    path('register', UserCreate.as_view(), name='register'),


] + router.urls
