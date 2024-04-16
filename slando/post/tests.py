import os
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from .models import *
from django.contrib.auth.models import User
from django.core.files import File



class SlandoAPITestCase(APITestCase):
    def setUp(self):
        user = User(username='testuser', email='test@test.com')
        user.set_password("testuserpassword")
        user.save()
        user_2 = User(username='testuser2', email='test2@test.com')
        user_2.set_password("testuserpassword2")
        user_2.save()
        category_test = Category.objects.create(
            name='test_category'
        )
        post = Post.objects.create(
            title='Test title',
            author=user,
            category=category_test,
            content='test_content',
            price=111,
            is_active=True,
        )

    def test_create_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 2)

    def test_single_post(self):
        post_count = Post.objects.count()
        self.assertEqual(post_count, 1)

    def test_single_category(self):
        category_count = Category.objects.count()
        self.assertEqual(category_count, 1)

    def test_get_list_post(self):
        data = {}
        url = api_reverse('post:posts-list')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_without_login(self):
        data = {
            "title": "Test title 2",
            "category": Category.objects.get(name='test_category').id,
            "price": 1111,
            "content": "tes_content2",
            "is_active": True
        }
        url = api_reverse('post:posts-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_with_login(self):
        data = {
            "title": "Test title 2",
            "category": Category.objects.get(name='test_category').id,
            "price": 1111,
            "content": "tes_content2",
            "is_active": True
        }
        url = api_reverse('post:posts-list')
        self.client.login(username='testuser2', password='testuserpassword2')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_post(self):
        post = Post.objects.first()
        data = {}
        url = post.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post_without_login(self):
        post = Post.objects.first()
        url = post.get_api_url()
        data = {
            "title": "Test title 3",
            "price": 2222,
            "content": "tes_content3",
            "is_active": True
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_user_is_not_author(self):
        post = Post.objects.first()
        url = post.get_api_url()
        data = {
            "title": "Test title 111",
            "category": Category.objects.get(name='test_category').id,
            "price": 1111,
            "content": "tes_content111",
            "is_active": True
        }
        self.client.login(username='testuser2', password='testuserpassword2')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_post_user_is_author(self):
        post = Post.objects.first()
        url = post.get_api_url()
        data = {
            "title": "Test title 111",
            "category": Category.objects.get(name='test_category').id,
            "price": 1111,
            "content": "tes_content111",
            "is_active": True
        }
        self.client.login(username='testuser', password='testuserpassword')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_author_is_authenticated_user(self):
        user_auth = User.objects.get(username='testuser2')
        data = {
            "title": "Test title 2",
            "category": Category.objects.get(name='test_category').id,
            "price": 1111,
            "content": "tes_content2",
            "is_active": True
        }
        url = api_reverse('post:posts-list')
        self.client.login(username='testuser2', password='testuserpassword2')
        response = self.client.post(url, data, format='json')
        self.assertEqual(Post.objects.last().author, user_auth)

    def test_registration_user(self):
        data = {
            'username': 'testuser5',
            'password': 'testuserpassword5',
            'email': 'testuser5@testuser.com',
        }
        url = api_reverse('post:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_add_image_to_post_without_login(self):
        image_path = os.path.join(settings.BASE_DIR, 'fixtures/test_image/', '30025882b.jpg')
        image = File(open(image_path, 'rb'))
        post = Post.objects.first()
        data = {
            'image_file': image,
            'post_image': post.id,
        }
        url = api_reverse('post:images-list')
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_image_to_post_user_is_not_author(self):
        image_path = os.path.join(settings.BASE_DIR, 'fixtures/test_image/', '30025882b.jpg')
        image = File(open(image_path, 'rb'))
        post = Post.objects.first()
        data = {
            'image_file': image,
            'post_image': post.id,
        }
        url = api_reverse('post:images-list')
        self.client.login(username='testuser2', password='testuserpassword2')
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_image_to_post_user_is_author(self):
        image_path = os.path.join(settings.BASE_DIR, 'fixtures/test_image/', '30025882b.jpg')
        image = File(open(image_path, 'rb'))
        post = Post.objects.first()
        data = {
            'image_file': image,
            'post_image': post.id,
        }
        url = api_reverse('post:images-list')
        self.client.login(username='testuser', password='testuserpassword')
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ImagePost.objects.count(), 1)

