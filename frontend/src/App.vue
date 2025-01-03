<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
      <nav>
        <div class="nav-left">
          <RouterLink to="/">Recipes</RouterLink>
        </div>
        <div class="nav-center">
          <RouterLink to="/">
            <h2>Recipe Box</h2>
          </RouterLink>
        </div>
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
    
    .nav-center {
      flex: 2;
      text-align: center;
      margin: 0;
      h2 {
        font-size: 3rem;
      }
    }

    a {
      font-size: 1.25rem;
      font-weight: 500;
      color: var(--color-primary);
      text-decoration: none;
      padding: 0.5rem 0;
      transition: border-bottom 0.4s;
      white-space: nowrap;
      border-bottom: 1px solid transparent;

      &:hover {
        border-bottom: 1px solid var(--color-primary-light);
      }

      &.router-link-active {
        border-bottom: 1px solid var(--color-primary);
      }
    }
  }
}

</style>
