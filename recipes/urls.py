from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'recipes', views.RecipeViewSet, basename='recipe')

urlpatterns = [
    path('recipes/categories', views.get_categories, name='recipe-categories'),
    path('', include(router.urls)),
]
