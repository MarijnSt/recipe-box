<template>
    <div class="recipe-list">
        <h2>Recipes</h2>
        <div v-if="loading">Loading...</div>
        <div v-else-if="error">Error: {{ error }}</div>
        <div v-else class="recipe-list__grid">
            <div v-if="recipes.length === 0">No recipes found</div>
            <div v-else>
                <div v-for="recipe in recipes" :key="recipe.id" class="recipe-list__card">
                    <h3>{{ recipe.title }}</h3>
                    <p>Created by: {{ recipe.created_by.username }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { RecipeService } from "@/services/RecipeService";
import type { Recipe } from "@/types/Recipe";

const recipes = ref<Recipe[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

const fetchRecipes = async () => {
  try {
    recipes.value = await RecipeService.getRecipes();
  } catch (err) {
    error.value = "Failed to fetch recipes";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchRecipes();
});
</script>

<style scoped>
.recipe-list {
  padding: 20px;
}

.recipes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.recipe-card {
  border: 1px solid #ddd;
  padding: 15px;
  border-radius: 8px;
}
</style>