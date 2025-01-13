<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const username = ref('')
const password = ref('')
const email = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

async function handleSubmit() {
  if (!username.value || !password.value || !email.value) {
    errorMessage.value = 'Please enter a username, password, and email'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    await authStore.register(username.value, password.value, email.value)

    // redirect to originally requested page or home
    const redirectPath = route.query.redirect?.toString() || '/'
    router.push(redirectPath)
  } catch (error) {
    errorMessage.value = 'Invalid username, password, or email'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <main class="register-page">
    <h1 class="register-page__title">Register</h1>
    
    <form @submit.prevent="handleSubmit" class="register-form">
      <div class="register-form__group">
        <label class="register-form__label" for="username">Username</label>
        <input
          id="username"
          v-model="username"
          type="text"
          required
          autocomplete="username"
          class="register-form__input"
        >
      </div>

      <div class="register-form__group">
        <label class="register-form__label" for="password">Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          required
          autocomplete="current-password"
          class="register-form__input"
        >
      </div>

      <div class="register-form__group">
        <label class="register-form__label" for="email">Email</label>
        <input
          id="email"
          v-model="email"
          type="email"
          required
          autocomplete="email"
          class="register-form__input"
        >
      </div>

      <p v-if="errorMessage" class="register-form__error">
        {{ errorMessage }}
      </p>

      <button 
        type="submit" 
        :disabled="isLoading"
        class="register-form__submit"
        :class="{ 'register-form__submit--loading': isLoading }"
      >
        {{ isLoading ? 'Registering...' : 'Register' }}
      </button>

      <p class="register-form__register">
        Already have an account? 
        <RouterLink to="/login" class="register-form__register-link">
          Login here
        </RouterLink>
      </p>
    </form>
  </main>
</template>

<style scoped lang="scss">
.register-page {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;

  &__title {
    margin-bottom: 2rem;
    text-align: center;
  }
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;

  &__group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  &__label {
    font-weight: 600;
    color: var(--color-text);
  }

  &__input {
    padding: 0.75rem;
    border: 1px solid var(--color-border);
    border-radius: 4px;
    font-size: 1rem;
    
    &:focus {
      outline: none;
      border-color: var(--color-primary);
    }
  }

  &__error {
    color: red;
    font-size: 0.875rem;
    margin: 0;
  }

  &__submit {
    background-color: var(--color-primary);
    color: white;
    border: none;
    border-radius: 4px;
    padding: 0.75rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s;

    &:hover {
      background-color: var(--color-primary-dark);
    }

    &:disabled {
      background-color: var(--color-border);
      cursor: not-allowed;
    }

    &--loading {
      opacity: 0.8;
    }
  }

  &__register {
    text-align: center;
    margin: 0;
    font-size: 0.875rem;
  }

  &__register-link {
    color: var(--color-primary);
    text-decoration: none;
    font-weight: 600;

    &:hover {
      text-decoration: underline;
    }
  }
}
</style>