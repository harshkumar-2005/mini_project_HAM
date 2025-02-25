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
            headers: {
                ...defaultHeaders,
                ...options.headers
            }
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || `API Error: ${response.statusText}`);
        }

        return data;
    } catch (error) {
        console.error('API Request failed:', error);
        throw error;
    }
}

const api = {
    login: (email, password) => 
        apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        }),
    
    enrollCourse: (courseId) =>
        apiRequest('/enroll', {
            method: 'POST',
            body: JSON.stringify({ course_id: courseId })
        }),
    
    bulkEnroll: (courseIds) =>
        apiRequest('/bulk-enroll', {
            method: 'POST',
            body: JSON.stringify({ course_ids: courseIds })
        }),
    
    getCourses: () =>
        apiRequest('/courses', {
            method: 'GET'
        }),
    
    getEnrollments: () =>
        apiRequest('/student/enrollments', {
            method: 'GET'
        })
}; 