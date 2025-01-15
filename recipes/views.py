from rest_framework import viewsets, permissions
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .constants import RecipeCategory

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        """unauthenticated users can list and retrieve recipes, but cannot create, update, or delete"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        """all recipes for list and retrieve actions, only recipes created by the current user for create, update, and delete actions"""
        if self.action in ['list', 'retrieve']:
            return Recipe.objects.all()

        return Recipe.objects.filter(created_by=self.request.user)

@api_view(['GET'])
def get_categories(request):
    return Response([
        {'value': category.value, 'label': category.name.title()} 
        for category in RecipeCategory
    ])