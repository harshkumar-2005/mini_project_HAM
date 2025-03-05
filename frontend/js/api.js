const API_BASE_URL = 'http://localhost:5000';

async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    const defaultHeaders = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
    };

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers: { ...defaultHeaders, ...options.headers }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "API request failed");
        }

        return response.json();
    } catch (error) {
        console.error("API Error:", error.message);
        throw error;
    }
}

const api = {
    login: (email, password) => 
        apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        }),
    
    getCourses: () => apiRequest('/courses', { method: 'GET' })
};