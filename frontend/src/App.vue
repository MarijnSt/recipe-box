<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
      <nav>
        <div class="nav-left">
          <RouterLink to="/">Recipes</RouterLink>
        </div>
        <h3>Recipe Box</h3>
        <div class="nav-right">
          <RouterLink to="/about">About</RouterLink>
          <RouterLink to="/login">Login</RouterLink>
          <RouterLink to="/search">Search</RouterLink>
        </div>
      </nav>
  </header>

  <RouterView />
</template>

<style scoped lang="scss">
header {
  padding: 2rem 0;
  margin-bottom: 2rem;
  
  nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
  
    a {
      color: var(--color-text);
      text-decoration: none;
      padding: 0.5rem 0;
      transition: 0.4s;
  
      &:hover {
        color: var(--color-primary);
      }
  
      &.router-link-active {
        border-bottom: 2px solid var(--color-text);
      }
    }
  }
}

</style>
