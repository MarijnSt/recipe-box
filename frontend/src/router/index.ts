import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useAuthStore } from '@/stores/auth';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    // {
    //   path: '/register',
    //   name: 'register',
    //   component: () => import('../views/RegisterView.vue'),
    // },
    // {
    //   path: '/login',
    //   name: 'login',
    //   component: () => import('../views/LoginView.vue'),
    // },
    // {
    //   path: "/account",
    //   name: "account",
    //   component: () => import('../views/AccountView.vue'),
    //   meta: {
    //     requiresAuth: true,
    //   },
    // },
    {
      path: '/recipe/:slug',
      name: 'recipe',
      component: () => import('../views/RecipeView.vue'),
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  // check auth status if we haven't already (e.g. on page load)
  if (!authStore.isAuthenticated && !authStore.isLoading) {
    await authStore.getUserInfo();
  }

  // redirect to login if not authenticated
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return {
      path: '/login',
      query: { redirect: to.fullPath },
    };
  }
});

export default router