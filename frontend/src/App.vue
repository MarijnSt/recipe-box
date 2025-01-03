<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
      <nav>
        <div class="nav-left">
          <RouterLink to="/">Recipes</RouterLink>
        </div>
        <h2>Recipe Box</h2>
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
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 2rem;
    
    .nav-left, .nav-right {
      display: flex;
      gap: 2rem;
      flex: 1;
      align-items: center;
    }
    
    .nav-left {
      justify-content: flex-start;
    }
    
    .nav-right {
      justify-content: flex-end;
    }
    
    h2 {
      flex: 2;
      text-align: center;
      margin: 0;
      font-size: 2.5rem;
      font-weight: 900;
    }

    a {
      font-size: 1.25rem;
      font-weight: 500;
      color: var(--color-text);
      text-decoration: none;
      padding: 0.5rem 0;
      transition: color 0.4s;
      white-space: nowrap;
      border-bottom: 1px solid transparent;

      &:hover {
        color: var(--color-text);
        border-bottom: 1px solid var(--color-text);
      }

      &.router-link-active {
        border-bottom: 1px solid var(--color-text);
      }
    }
  }
}

</style>
