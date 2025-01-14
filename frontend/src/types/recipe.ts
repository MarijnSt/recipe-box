import type { User } from './User'

export interface Recipe {
    id: number;
    title: string;
    slug: string;
    category: string;
    ingredients: string;
    instruction: string;
    cooking_time: number;
    image: string;
    created_by: User;
    // is_saved?: boolean;
}