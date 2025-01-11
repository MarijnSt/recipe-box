from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Recipe
from PIL import Image
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class RecipeTests(TestCase):
    def setUp(self):
        # create test users
        self.user1 = User.objects.create_user(username='testuser1', password='testpass1')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')

        # create test client
        self.client = APIClient()

        # create test recipe
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            slug='test-recipe',
            ingredients='Test Ingredients', 
            instruction='Test Instructions', 
            cooking_time=10, 
            image='test.jpg',
            created_by=self.user1
        )

        # create temporary image file
        image = Image.new('RGB', (100, 100), color='red')
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        # recipe data used in tests where we create new recipes
        self.recipe_data = {
            'title': 'Second Recipe',
            'slug': 'second-recipe',
            'ingredients': 'Second Ingredients',
            'instruction': 'Second Instructions',
            'cooking_time': 15,
            'image': SimpleUploadedFile(
                name='test.jpg',
                content=tmp_file.read(),
                content_type='image/jpeg'
            )
        }

    def tearDown(self):
        # clean up any test images
        for recipe in Recipe.objects.all():
            if recipe.image:
                try:
                    os.remove(recipe.image.path)
                except Exception as e:
                    pass

    def test_can_get_recipe_list_unauthenticated(self):
        """Unauthenticated users can get recipe list"""
        response = self.client.get(reverse('recipe-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Recipe')

    def test_can_get_recipe_detail_unauthenticated(self):
        """Unauthenticated users can get recipe detail"""
        response = self.client.get(reverse('recipe-detail', args=[self.recipe.slug]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Recipe')

    def test_cannot_create_recipe_unauthenticated(self):
        """Unauthenticated users cannot create recipe"""
        response = self.client.post(reverse('recipe-list'), self.recipe_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_create_recipe_authenticated(self):
        """Authenticated users can create recipe"""
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.post(reverse('recipe-list'), self.recipe_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 2)
        self.assertEqual(Recipe.objects.latest('id').title, 'Second Recipe')
        self.assertEqual(Recipe.objects.latest('id').created_by, self.user1)

    def test_can_update_own_recipe(self):
        """Authenticated users can update their own recipe"""
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.put(reverse('recipe-detail', args=[self.recipe.slug]), self.recipe_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, 'Second Recipe')
        self.assertEqual(self.recipe.ingredients, 'Second Ingredients')
        self.assertEqual(self.recipe.instruction, 'Second Instructions')
        self.assertEqual(self.recipe.cooking_time, 15)

    def test_cannot_update_other_users_recipe(self):
        """Authenticated users cannot update other users recipe"""
        self.client.login(username='testuser2', password='testpass2')
        response = self.client.put(reverse('recipe-detail', args=[self.recipe.slug]), self.recipe_data)
        # response code will be a 404 instead of 403 because queryset is filtered by created_by
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, 'Test Recipe')
        self.assertEqual(self.recipe.ingredients, 'Test Ingredients')
        self.assertEqual(self.recipe.instruction, 'Test Instructions')
        self.assertEqual(self.recipe.cooking_time, 10)

    def test_can_delete_own_recipe(self):
        """Authenticated users can delete their own recipe"""
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.delete(reverse('recipe-detail', args=[self.recipe.slug]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 0)

    def test_cannot_delete_other_users_recipe(self):
        """Authenticated users cannot delete other users recipe"""
        self.client.login(username='testuser2', password='testpass2')
        response = self.client.delete(reverse('recipe-detail', args=[self.recipe.slug]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Recipe.objects.count(), 1)
