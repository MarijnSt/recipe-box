import type { Recipe } from "@/types/Recipe";

export const RecipeService = {
  async getRecipes(): Promise<Recipe[]> {
    const response = await fetch("http://localhost:8000/api/recipes");
    return response.json();
  },
};
