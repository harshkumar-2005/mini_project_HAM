const API_BASE_URL = 'http://localhost:5000';

async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    const defaultHeaders = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
    };

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers
        }
    });

    if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`);
    }

    return response.json();
}

const api = {
    login: (email, password) => 
        apiRequest('/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        }),
    
    enrollCourse: (courseId) =>
        apiRequest('/enroll', {
            method: 'POST',
            body: JSON.stringify({ course_id: courseId })
        }),
    
    getCourses: () =>
        apiRequest('/courses', {
            method: 'GET'
        }),
    
    getEnrollments: () =>
        apiRequest('/enrollments', {
            method: 'GET'
        })
}; 