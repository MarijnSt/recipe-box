<template>
    <div class="recipe-list">
        <div v-if="loading" class="loading">Loading...</div>
        <div v-else-if="error" class="error">Error: {{ error }}</div>
        <div v-else>
            <div v-if="recipes.length === 0" class="no-recipes">No recipes found</div>
            <div v-else class="recipe-grid">
                <RecipeCard
                    v-for="recipe in recipes"
                    :key="recipe.id"
                    :recipe="recipe"
                />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { RecipeService } from "@/services/RecipeService";
import type { Recipe } from "@/types/Recipe";
import RecipeCard from './RecipeCard.vue';

const recipes = ref<Recipe[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

const fetchRecipes = async () => {
    loading.value = true;
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

<style scoped lang="scss">
.recipe-list {
    max-width: var(--max-width, 1280px);
    margin: 0 auto;
    padding: 0 2rem;
}

.recipe-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
    margin: 2rem 0;
}

.loading,
.error,
.no-recipes {
    text-align: center;
    padding: 2rem;
    font-size: 1.2rem;
    color: var(--color-text);
}

.error {
    color: red;
}
</style>