import type { Recipe } from "@/types/Recipe";
import type { RecipeCategory } from "@/types/RecipeCategory";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

export const RecipeService = {
  async getCategories(): Promise<RecipeCategory[]> {
    const response = await fetch(`${apiBaseUrl}/recipes/categories`);
    if (!response.ok) {
      throw new Error('Failed to fetch categories');
    }
    return response.json();
  },

  async getRecipes(): Promise<Recipe[]> {
    const response = await fetch(`${apiBaseUrl}/recipes/`);
    return response.json();
  },
  
  async getRecipe(slug: string): Promise<Recipe> {
    const response = await fetch(`${apiBaseUrl}/recipes/${slug}/`);
    if (!response.ok) {
      throw new Error('Recipe not found');
    }
    return response.json();
  },
};
