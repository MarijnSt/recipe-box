<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import SearchIcon from '@/components/icons/SearchIcon.vue'
import UserIcon from '@/components/icons/UserIcon.vue'
const isMenuOpen = ref(false)

function toggleMenu() {
  isMenuOpen.value = !isMenuOpen.value
}
</script>

<template>
  <header>
      <nav>
        <RouterLink to="/" class="nav-center">
          <h2>Recipe Box</h2>
        </RouterLink>
        <div class="nav-right">
          <RouterLink to="/search">
            <SearchIcon />
          </RouterLink>
          <RouterLink to="/login">
            <UserIcon />
          </RouterLink>
        </div>
      </nav>
  </header>

  <RouterView />
</template>

<style scoped lang="scss">
header nav {
  max-width: var(--container-width);
  padding: var(--container-padding);
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;

  .nav-right {
    position: absolute;
    right: var(--container-padding);
    display: flex;
    align-items: center;
    gap: 1rem;

    a {
      height: var(--icon-size);
    }
  }
}

@media (max-width: 768px) {
  header nav {
    justify-content: left;
  }
}
</style>
