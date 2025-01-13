<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
const authStore = useAuthStore()
const router = useRouter()
function logout() {
    try {
        authStore.logout()
        router.push('/')
    } catch (error) {
        console.error('Logout failed', error)
    }
}
</script>

<template>
  <main class="profile-page">
    <h1 class="profile-page__title">Profile</h1>
    <button class="profile-page__logout" @click="logout">Logout</button>
  </main>
</template>

<style scoped lang="scss">
.profile-page {
  display: flex;
  flex-direction: column;
  align-items: center;

  &__logout {
    margin-top: 1rem;
    background-color: var(--color-primary);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
    transition: background-color 0.2s ease;

    &:hover {
      background-color: var(--color-primary-dark);
    }
  }
}
</style>
