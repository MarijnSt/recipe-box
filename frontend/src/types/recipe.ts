import type { User } from './User'

export interface Recipe {
    id: number;
    title: string;
    ingredients: string;
    instruction: string;
    cooking_time: number;
    created_by: User;
}