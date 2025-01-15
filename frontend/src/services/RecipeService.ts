import type { Recipe } from "@/types/Recipe";
import type { RecipeCategory } from "@/types/RecipeCategory";

export const RecipeService = {
  async getCategories(): Promise<RecipeCategory[]> {
    const response = await fetch("http://localhost:8000/api/recipes/categories");
    if (!response.ok) {
      throw new Error('Failed to fetch categories');
    }
    return response.json();
  },

  async getRecipes(): Promise<Recipe[]> {
    const response = await fetch("http://localhost:8000/api/recipes");
    return response.json();
  },
  
  async getRecipe(slug: string): Promise<Recipe> {
    const response = await fetch(`http://localhost:8000/api/recipes/${slug}`);
    if (!response.ok) {
      throw new Error('Recipe not found');
    }
    return response.json();
  },
};
