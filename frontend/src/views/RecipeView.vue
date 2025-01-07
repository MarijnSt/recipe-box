<template>
  <div class="recipe" v-if="recipe">
    <h1>{{ recipe.title }}</h1>
    <div class="recipe-content">
      <img :src="recipe.image" :alt="recipe.title" class="recipe-image">
      <div class="recipe-details">
        <div class="cooking-time">
          <h3>Cooking Time</h3>
          <p>{{ recipe.cooking_time }} minutes</p>
        </div>
        <div class="ingredients">
          <h3>Ingredients</h3>
          <p>{{ recipe.ingredients }}</p>
        </div>
        <div class="instructions">
          <h3>Instructions</h3>
          <p>{{ recipe.instruction }}</p>
        </div>
        <div class="author">
          <p>Created by: {{ recipe.created_by.username }}</p>
        </div>
      </div>
    </div>
  </div>
  <div v-else-if="loading" class="loading">Loading...</div>
  <div v-else-if="error" class="error">{{ error }}</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import type { Recipe } from '@/types/Recipe'
import { RecipeService } from '@/services/RecipeService'

const route = useRoute()
const recipe = ref<Recipe | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  const id = route.params.id as string
  try {
    recipe.value = await RecipeService.getRecipe(id)
  } catch (err) {
    error.value = 'Failed to load recipe'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped lang="scss">
.recipe {
  max-width: var(--max-width, 1280px);
  margin: 0 auto;
  padding: 2rem;

  h1 {
    margin-bottom: 2rem;
    text-align: center;
  }
}

.recipe-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: start;
}

.recipe-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.recipe-details {
  display: flex;
  flex-direction: column;
  gap: 2rem;

  h3 {
    color: var(--color-primary);
    margin-bottom: 0.5rem;
  }

  .author {
    margin-top: auto;
    font-style: italic;
    color: var(--color-text);
  }
}

.loading,
.error {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
}

.error {
  color: red;
}

@media (max-width: 768px) {
  .recipe-content {
    grid-template-columns: 1fr;
  }
}
</style> 