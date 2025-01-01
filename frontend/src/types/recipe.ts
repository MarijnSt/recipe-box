import type { User } from "./user";

export interface Recipe {
    id: number;
    title: string;
    ingredients: string;
    instruction: string;
    cooking_time: number;
    created_by: User;
}