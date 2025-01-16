<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { RecipeService } from "@/services/RecipeService";
import type { Recipe } from "@/types/Recipe";
import type { RecipeCategory } from "@/types/RecipeCategory";
import RecipeCard from './RecipeCard.vue';
import { useAuthStore } from '@/stores/auth';

const currentPage = ref(1);
const totalPages = ref(1);
const pageSize = 10;
const totalRecipes = ref(0);

const categories = ref<RecipeCategory[]>([]);
const selectedCategories = ref<Set<string>>(new Set());
const recipes = ref<Recipe[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const showMyRecipes = ref(false);
// const showSavedRecipes = ref(false);

const authStore = useAuthStore();

const fetchCategories = async () => {
    try {
        categories.value = await RecipeService.getCategories();
    } catch (err) {
        console.error("Failed to fetch categories",err);
    }
}

const fetchRecipes = async () => {
    loading.value = true;
    try {
        const filters = {
            page: currentPage.value,
            page_size: pageSize,
            ...(selectedCategories.value.size > 0 && { categories: Array.from(selectedCategories.value) }),
            ...(showMyRecipes.value && authStore.user && { created_by: authStore.user.id })
        }
        const response = await RecipeService.getRecipes(filters);
        recipes.value = response.results;
        totalRecipes.value = response.count;
        totalPages.value = Math.ceil(totalRecipes.value / pageSize);
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


onMounted(() => {
    fetchCategories();
    fetchRecipes();
});

watch([selectedCategories, showMyRecipes], () => {
    currentPage.value = 1; // Reset to first page when filters change
    fetchRecipes();
});

watch(currentPage, () => {
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
            <div v-if="recipes.length === 0" class="no-recipes">No recipes found</div>
            <div v-else class="recipe-grid">
                <RecipeCard
                    v-for="recipe in recipes"
                    :key="recipe.id"
                    :recipe="recipe"
                />
                <div v-if="totalPages > 1" class="pagination">
                    <button 
                    :disabled="currentPage === 1"
                    @click="currentPage--"
                    class="pagination__button"
                    >
                        Previous
                    </button>
                    <span class="pagination__info">
                        Page {{ currentPage }} of {{ totalPages }}
                    </span>
                    <button 
                    :disabled="currentPage === totalPages"
                    @click="currentPage++"
                    class="pagination__button"
                    >
                        Next
                    </button>
                </div>
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