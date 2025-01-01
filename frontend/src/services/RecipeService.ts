import type { Recipe } from "@/types/Recipe";

export const RecipeService = {
  async getRecipes(): Promise<Recipe[]> {
    const response = await fetch("http://localhost:3000/recipes");
    return response.json();
  },
};
