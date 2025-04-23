import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface LoginCredentials {
    correo: string;
    clave: string;
}

interface LoginResponse {
    access_token: string;
}

export const authService = {
    async login(credentials: LoginCredentials): Promise<LoginResponse> {
        try {
            const { data } = await axios.post<LoginResponse>(
                `${API_URL}/auth/token`,
                credentials
            );
            return data;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                throw new Error(error.response?.data?.message || 'Error en la autenticación');
            }
            throw new Error('Error inesperado durante el login');
        }
    }
}; 