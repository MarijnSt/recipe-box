from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .constants import RecipeCategory

class RecipePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    lookup_field = 'slug'
    pagination_class = RecipePagination
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
            queryset = Recipe.objects.all()

            # Filter by category
            category = self.request.query_params.get('category', None)
            if category:
                queryset = queryset.filter(category=category)

            # Filter by user
            user = self.request.query_params.get('created_by', None)
            if user:
                queryset = queryset.filter(created_by=user)

            return queryset

        return Recipe.objects.filter(created_by=self.request.user)

@api_view(['GET'])
def get_categories(request):
    return Response([
        {'value': category.value, 'label': category.name.title()} 
        for category in RecipeCategory
    ])