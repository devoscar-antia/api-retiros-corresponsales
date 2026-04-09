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
                const data = error.response?.data as
                    | { detail?: string | Array<{ msg?: string }> }
                    | undefined;
                let msg = 'Error en la autenticación';
                if (typeof data?.detail === 'string') {
                    msg = data.detail;
                } else if (Array.isArray(data?.detail) && data.detail[0]?.msg) {
                    msg = data.detail[0].msg;
                }
                throw new Error(msg);
            }
            throw new Error('Error inesperado durante el login');
        }
    }
}; 