export interface PaginatedResponse<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
}

export interface PaginationOptions {
    page?: number;
    page_size?: number;
}

export interface RecipeFilters extends PaginationOptions {
    categories?: string[];
    created_by?: number;
}