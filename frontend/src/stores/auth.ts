import { defineStore } from "pinia";
import { ref } from "vue";
import type { User } from "@/types/User";
import { AuthService } from "@/services/AuthService";

export const useAuthStore = defineStore("auth", () => {
    const user = ref<User | null>(null);
    const isLoading = ref(false);
    const error = ref<string | null>(null);
    const isAuthenticated = ref(false);

    async function register(username: string, email: string, password: string) {
        isLoading.value = true;
        error.value = null;

        try {
            user.value = await AuthService.register(username, email, password);
            isAuthenticated.value = true;
        } catch (e) {
            error.value = e instanceof Error ? e.message : "Registration failed";
            throw e;
        } finally {
            isLoading.value = false;
        }
    }

    async function login(username: string, password: string) {
        isLoading.value = true;
        error.value = null;

        try {
            user.value = await AuthService.login(username, password);
            isAuthenticated.value = true;
        } catch (e) {
            error.value = e instanceof Error ? e.message : "Login failed";
            throw e;
        } finally {
            isLoading.value = false;
        }
    }

    async function logout() {
        isLoading.value = true;
        error.value = null;

        try {
            await AuthService.logout();
            user.value = null;
            isAuthenticated.value = false;
        } catch (e) {
            error.value = e instanceof Error ? e.message : "Logout failed";
            throw e;
        } finally {
            isLoading.value = false;
        }
    }

    async function getUserInfo() {
        isLoading.value = true;
        error.value = null;

        try {
            user.value = await AuthService.getUserInfo();
        } catch (e) {
            error.value = e instanceof Error ? e.message : "Failed to get user info";
            throw e;
        } finally {
            isLoading.value = false;
        }
    }

    return {
        user,
        isLoading,
        error,
        isAuthenticated,
        register,
        login,
        logout,
        getUserInfo,
    };
});
