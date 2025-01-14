<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { RecipeService } from "@/services/RecipeService";
import type { Recipe } from "@/types/Recipe";
import RecipeCard from './RecipeCard.vue';
import { useAuthStore } from '@/stores/auth';

const recipes = ref<Recipe[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const selectedCategories = ref<Set<string>>(new Set());
const showMyRecipes = ref(false);
// const showSavedRecipes = ref(false);

const authStore = useAuthStore();

const categories = [
    { value: 'breakfast', label: 'Breakfast' },
    { value: 'lunch', label: 'Lunch' },
    { value: 'dinner', label: 'Dinner' },
    { value: 'snack', label: 'Snack' },
    { value: 'dessert', label: 'Dessert' },
    { value: 'drink', label: 'Drink' },
    { value: 'other', label: 'Other' }
];

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

const toggleCategory = (category: string) => {
    if (selectedCategories.value.has(category)) {
        selectedCategories.value.delete(category);
    } else {
        selectedCategories.value.add(category);
    }
    selectedCategories.value = new Set(selectedCategories.value); // Trigger reactivity
};

const filteredRecipes = computed(() => {
    let filtered = recipes.value;

    // Apply category filters
    if (selectedCategories.value.size > 0) {
        filtered = filtered.filter(recipe => selectedCategories.value.has(recipe.category));
    }

    // Apply user filters
    if (showMyRecipes.value) {
        filtered = filtered.filter(recipe => recipe.created_by.id === authStore.user?.id);
    }
    // if (showSavedRecipes.value) {
    //     filtered = filtered.filter(recipe => recipe.is_saved);
    // }

    return filtered;
});

onMounted(() => {
    fetchRecipes();
});
</script>

<template>
    <div class="recipe-list">
        <div class="filters">
            <div class="category-filter">
                <button
                    v-for="category in categories"
                    :key="category.value"
                    :class="['filter-btn', { active: selectedCategories.has(category.value) }]"
                    @click="toggleCategory(category.value)"
                >
                    {{ category.label }}
                </button>
            </div>
            <div v-if="authStore.isAuthenticated" class="user-filter">
                <button
                    class="filter-btn"
                    :class="{ active: showMyRecipes }"
                    @click="showMyRecipes = !showMyRecipes"
                >
                    My Recipes
                </button>
                <!-- <button
                    class="filter-btn"
                    :class="{ active: showSavedRecipes }"
                    @click="showSavedRecipes = !showSavedRecipes"
                >
                    Saved Recipes
                </button> -->
            </div>
        </div>
        <div v-if="loading" class="loading">Loading...</div>
        <div v-else-if="error" class="error">Error: {{ error }}</div>
        <div v-else>
            <div v-if="filteredRecipes.length === 0" class="no-recipes">No recipes found</div>
            <div v-else class="recipe-grid">
                <RecipeCard
                    v-for="recipe in filteredRecipes"
                    :key="recipe.id"
                    :recipe="recipe"
                />
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
.recipe-list {
    max-width: var(--container-max-width);
    margin: 0 auto;
    padding: 0 var(--container-padding);
}

.filters {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-start;
    margin: 1rem 0;
    padding: 1rem 0;
    gap: 1rem;
}

.category-filter,
.user-filter {
    display: flex;
    gap: 0.5rem;
}

.user-filter {
    padding-top: 1rem;
    width: 100%;
}


.category-filter {
    flex-wrap: wrap;
}

.filter-btn {
    padding: 0.5rem 1rem;
    border: 1px solid var(--color-border);
    border-radius: 20px;
    background: transparent;
    color: var(--color-text);
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;

    &:hover {
        background: var(--color-border);
    }

    &.active {
        background: var(--color-primary);
        color: var(--color-white);
        border-color: var(--color-primary);
    }
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

@include breakpoint(sm) {
    .filters {
        flex-direction: row;
        align-items: center;
    }

    .user-filter {
        padding-top: 0;
        width: unset;
    }
}
</style>