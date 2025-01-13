import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RecipeView from '../views/RecipeView.vue'
import SearchView from '../views/SearchView.vue'
import NotFoundView from '../views/NotFoundView.vue'
import { useAuthStore } from '@/stores/auth';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    // {
    //   path: '/register',
    //   name: 'register',
    //   component: () => import('../views/RegisterView.vue'),
    // },
    // {
    //   path: "/profile",
    //   name: "profile",
    //   component: () => import('../views/ProfileView.vue'),
    //   meta: {
    //     requiresAuth: true,
    //   },
    // },
    {
      path: '/recipe/:slug',
      name: 'recipe',
      component: RecipeView,
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView,
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFoundView,
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

  next();
});

export default router