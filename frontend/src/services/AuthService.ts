import type { User } from "@/types/User";

export const AuthService = {
    async getCsrfToken(): Promise<string> {
        const response = await fetch("http://localhost:8000/api/auth/csrf/", {
            credentials: "include",
        });
        const data = await response.json();
        return data.csrfToken;
    },

    async register(username: string, password: string, email: string): Promise<User> {
        const response = await fetch("http://localhost:8000/api/auth/register/", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": await this.getCsrfToken(),
            },
            body: JSON.stringify({ username, password, email }),
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message || "Failed to register");
        }

        const data = await response.json();
        return data.user;
    },

    async login(username: string, password: string): Promise<User> {
        const response = await fetch("http://localhost:8000/api/auth/login/", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": await this.getCsrfToken(),
            },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message || "Failed to login");
        }

        const data = await response.json();
        return data.user;
    },

    async logout(): Promise<void> {
        const response = await fetch("http://localhost:8000/api/auth/logout", {
            method: "POST",
            credentials: "include",
            headers: {
                "X-CSRFToken": await this.getCsrfToken(),
            },
        });

        if (!response.ok) {
            throw new Error("Failed to logout");
        }

        const data = await response.json();
        return data.message;
    },

    async getUserInfo(): Promise<User> {
        const response = await fetch("http://localhost:8000/api/auth/user", {
            credentials: "include",
        });

        if (!response.ok) {
            throw new Error("Failed to get user info");
        }

        const data = await response.json();
        return data;
    },
};

