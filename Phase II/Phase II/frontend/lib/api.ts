const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export interface Task {
    id: number;
    title: string;
    description?: string;
    completed: boolean;
    created_at: string;
    user_id: string;
}

export interface CreateTaskDto {
    title: string;
    description?: string;
}

export interface UpdateTaskDto {
    title?: string;
    description?: string;
    completed?: boolean;
}

class ApiClient {
    private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
        const token = localStorage.getItem('auth_token'); // TODO: Replace with Better Auth token retrieval

        const headers: HeadersInit = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        if (token) {
            // headers['Authorization'] = `Bearer ${token}`; 
            // Better Auth might handle this differently, but for now assuming Bearer
        }

        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers,
        });

        if (!response.ok) {
            if (response.status === 401) {
                // Handle unauthorized
                window.location.href = '/auth';
            }
            throw new Error(`API Error: ${response.statusText}`);
        }

        if (response.status === 204) {
            return {} as T;
        }

        return response.json();
    }

    async getTasks(status?: 'all' | 'pending' | 'completed'): Promise<Task[]> {
        const query = status ? `?status=${status}` : '';
        return this.request<Task[]>(`/tasks${query}`);
    }

    async createTask(data: CreateTaskDto): Promise<Task> {
        return this.request<Task>('/tasks', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async updateTask(id: number, data: UpdateTaskDto): Promise<Task> {
        return this.request<Task>(`/tasks/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    async toggleTaskComplete(id: number): Promise<Task> {
        return this.request<Task>(`/tasks/${id}/complete`, {
            method: 'PATCH'
        });
    }

    async deleteTask(id: number): Promise<void> {
        return this.request<void>(`/tasks/${id}`, {
            method: 'DELETE',
        });
    }
}

export const api = new ApiClient();
