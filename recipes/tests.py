from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Recipe

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
            ingredients='Test Ingredients', 
            instruction='Test Instructions', 
            cooking_time=10, 
            created_by=self.user1
        )

    def test_can_get_recipe_list_unauthenticated(self):
        """Unauthenticated users can get recipe list"""
        response = self.client.get(reverse('recipe-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Recipe')

    def test_can_get_recipe_detail_unauthenticated(self):
        """Unauthenticated users can get recipe detail"""
        response = self.client.get(reverse('recipe-detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Recipe')

    def test_cannot_create_recipe_unauthenticated(self):
        """Unauthenticated users cannot create recipe"""
        new_recipe = {
            'title': 'New Recipe',
            'ingredients': 'New Ingredients',
            'instruction': 'New Instructions',
            'cooking_time': 15
        }
        response = self.client.post(reverse('recipe-list'), new_recipe)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_create_recipe_authenticated(self):
        """Authenticated users can create recipe"""
        self.client.login(username='testuser1', password='testpass1')
        new_recipe = {
            'title': 'New Recipe',
            'ingredients': 'New Ingredients',
            'instruction': 'New Instructions',
            'cooking_time': 15
        }
        response = self.client.post(reverse('recipe-list'), new_recipe)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 2)
        self.assertEqual(Recipe.objects.latest('id').title, 'New Recipe')
        self.assertEqual(Recipe.objects.latest('id').created_by, self.user1)

    def test_can_update_own_recipe(self):
        """Authenticated users can update their own recipe"""
        self.client.login(username='testuser1', password='testpass1')
        updated_recipe = {
            'title': 'Updated Recipe',
            'ingredients': 'Updated Ingredients',
            'instruction': 'Updated Instructions',
            'cooking_time': 20
        }
        response = self.client.put(reverse('recipe-detail', args=[self.recipe.id]), updated_recipe)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, 'Updated Recipe')
        self.assertEqual(self.recipe.ingredients, 'Updated Ingredients')
        self.assertEqual(self.recipe.instruction, 'Updated Instructions')
        self.assertEqual(self.recipe.cooking_time, 20)

    def test_cannot_update_other_users_recipe(self):
        """Authenticated users cannot update other users recipe"""
        self.client.login(username='testuser2', password='testpass2')
        updated_recipe = {
            'title': 'Updated Recipe',
            'ingredients': 'Updated Ingredients',
            'instruction': 'Updated Instructions',
            'cooking_time': 20
        }
        response = self.client.put(reverse('recipe-detail', args=[self.recipe.id]), updated_recipe)
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
        response = self.client.delete(reverse('recipe-detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 0)

    def test_cannot_delete_other_users_recipe(self):
        """Authenticated users cannot delete other users recipe"""
        self.client.login(username='testuser2', password='testpass2')
        response = self.client.delete(reverse('recipe-detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Recipe.objects.count(), 1)
