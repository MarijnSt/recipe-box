import type { Recipe } from "@/types/Recipe";

export const RecipeService = {
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
