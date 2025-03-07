const API_BASE_URL = "http://127.0.0.1:5000";

async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem("token");
    const defaultHeaders = {
        "Content-Type": "application/json",
        ...(token && { "Authorization": `Bearer ${token}` })
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
    login: (email, password) => apiRequest("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password })
    }),

    getCourses: () => apiRequest("/courses", { method: "GET" }),

    addCourse: (name, description, prerequisiteId) => apiRequest("/add_course", {
        method: "POST",
        body: JSON.stringify({ name, description, prerequisite_id: prerequisiteId })
    }),

    enrollCourse: (courseId) => apiRequest("/enroll", {
        method: "POST",
        body: JSON.stringify({ course_id: courseId })
    })
};

export default api;
