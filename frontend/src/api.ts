export interface Category {
    id: number;
    name: string;
}

export interface Task {
    id: number;
    name: string;
    category_id?: number;
}

async function jsonFetch<T>(url: string): Promise<T> {
    const res = await fetch(url);
    if (!res.ok) {
        throw new Error(`Ошибка ${res.status}`);
    }
    return res.json();
}

export const api = {
    getCategories: () => jsonFetch<Category[]>("/categories"),
    getTasks: () => jsonFetch<Task[]>("/tasks"),
    getTasksByCategory: (categoryId: number) =>
        jsonFetch<Task[]>(`/tasks/tasks/${categoryId}`)
};
