import type { Recipe } from "@/types/Recipe";
import type { RecipeCategory } from "@/types/RecipeCategory";
import type { PaginatedResponse, PaginationOptions, RecipeFilters } from "@/types/Api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const RecipeService = {
  async getCategories(): Promise<RecipeCategory[]> {
    const response = await fetch(`${API_BASE_URL}/recipes/categories`);
    if (!response.ok) {
      throw new Error('Failed to fetch categories');
    }
    return response.json();
  },

  async getRecipes(filters: RecipeFilters = {}): Promise<PaginatedResponse<Recipe>> {
    const params = new URLSearchParams();

    if (filters.page) params.append("page", filters.page.toString());
    if (filters.page_size) params.append("page_size", filters.page_size.toString());
    if (filters.categories?.length) params.append("categories", filters.categories.join(','));
    if (filters.created_by) params.append("created_by", filters.created_by);

    const response = await fetch(`${API_BASE_URL}/recipes/?${params.toString()}`);

    if (!response.ok) {
      throw new Error('Failed to fetch recipes');
    }
    return response.json();
  },
  
  async getRecipe(slug: string): Promise<Recipe> {
    const response = await fetch(`${API_BASE_URL}/recipes/${slug}/`);
    if (!response.ok) {
      throw new Error('Recipe not found');
    }
    return response.json();
  },
};
