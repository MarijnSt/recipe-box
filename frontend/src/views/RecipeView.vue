<template>
  <div class="recipe" v-if="recipe">
    <div class="recipe__hero">
      <img :src="recipe.image" :alt="recipe.title" class="recipe__image">
    </div>
    <div class="recipe__content">
      <div class="recipe__header">
        <h1 class="recipe__title">{{ recipe.title }}</h1>
        <div class="recipe__meta">
          <span class="recipe__time">
            <i class="recipe__icon">⏱</i> {{ recipe.cooking_time }} minutes
          </span>
          <span class="recipe__author">
            <i class="recipe__icon">✍︎</i> {{ recipe.created_by.username }}
          </span>
        </div>
      </div>
      <div class="recipe__details">
        <div class="recipe__ingredients">
          <h3 class="recipe__subtitle">Ingredients</h3>
          <p class="recipe__text">{{ recipe.ingredients }}</p>
        </div>
        <div class="recipe__instructions">
          <h3 class="recipe__subtitle">Instructions</h3>
          <p class="recipe__text">{{ recipe.instruction }}</p>
        </div>
      </div>
    </div>
  </div>
  <div v-else-if="loading" class="recipe--loading">Loading...</div>
  <div v-else-if="error" class="recipe--error">{{ error }}</div>
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

  &__hero {
    width: 100%;
    height: 40vh;
    min-height: 300px;
    max-height: 500px;
    overflow: hidden;
    margin-bottom: 3rem;
  }

  &__image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  &__content {
    padding: 0 2rem;
  }

  &__header {
    text-align: center;
    margin-bottom: 4rem;
  }

  &__title {
    margin-bottom: 1rem;
    font-family: var(--font-family-heading);
    font-weight: 900;
  }

  &__meta {
    display: flex;
    justify-content: center;
    gap: 2rem;
    color: var(--color-text);
    font-size: 1.1rem;
  }

  &__time,
  &__author {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  &__icon {
    font-style: normal;
  }

  &__details {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 4rem;
    margin: 0 auto;
    max-width: 1000px;
  }

  &__subtitle {
    color: var(--color-primary);
    margin-bottom: 1.5rem;
    font-family: var(--font-family-heading);
    font-size: 1.75rem;
  }

  &__text {
    white-space: pre-line;
    line-height: 1.8;
  }

  &--loading,
  &--error {
    text-align: center;
    padding: 2rem;
    font-size: 1.2rem;
  }

  &--error {
    color: red;
  }
}

@media (max-width: 768px) {
  .recipe {
    &__details {
      grid-template-columns: 1fr;
      gap: 2rem;
    }

    &__hero {
      height: 30vh;
      min-height: 200px;
    }
  }
}
</style> 