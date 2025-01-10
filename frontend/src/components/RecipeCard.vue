<template>
  <RouterLink :to="{ name: 'recipe', params: { slug: recipe.slug }}" class="recipe-card">
    <div class="recipe-card__image">
      <img :src="recipe.image" :alt="recipe.title">
    </div>
    <div class="recipe-card__content">
      <h3>{{ recipe.title }}</h3>
      <RouterLink :to="{ name: 'recipe', params: { slug: recipe.slug }}" class="see-recipe">
        See Recipe
        <span class="arrow">→</span>
      </RouterLink>
    </div>
  </RouterLink>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { Recipe } from '@/types/Recipe'

defineProps<{
  recipe: Recipe
}>()
</script>

<style scoped lang="scss">
.recipe-card {
  display: block;
  text-decoration: none;
  color: inherit;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease;
  height: 100%;

  &:hover {
    transform: translateY(-4px);

    .see-recipe {
      .arrow {
        transform: translateX(4px);
      }
    }
  }

  &__image {
    position: relative;
    padding-top: 75%; // 4:3 aspect ratio
    overflow: hidden;

    img {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  &__content {
    padding: 1.5rem 0;
    border-top: 2px solid var(--color-primary);

    h3 {
      margin: 0 0 1rem;
      font-size: 1.5rem;
      line-height: 1.2;
      color: var(--color-primary);
    }
  }
}

.see-recipe {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--color-text);
  text-decoration: none;

  .arrow {
    transition: transform 0.3s ease;
  }
}
</style> 