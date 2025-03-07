import api from "./api.js";
import { checkAuth, logout } from "./auth.js";

document.addEventListener("DOMContentLoaded", async () => {
    await checkAuth();
    const userRole = localStorage.getItem("userRole");

    if (userRole !== "student") {
        alert("Unauthorized Access");
        window.location.href = "/index.html";
        return;
    }

    loadCourses();

    document.getElementById("logoutBtn").addEventListener("click", logout);
});

async function loadCourses() {
    try {
        const courses = await api.getCourses();
        const coursesList = document.getElementById("coursesList");

        if (!courses.length) {
            coursesList.innerHTML = '<div class="empty-state">No courses available</div>';
            return;
        }

        coursesList.innerHTML = courses.map(course => `
            <div class="course-card">
                <h3>${course.name}</h3>
                <p>${course.description || "No description available"}</p>
                <button class="enroll-btn" data-course-id="${course.id}">Enroll</button>
            </div>
        `).join("");

        document.querySelectorAll(".enroll-btn").forEach(button => {
            button.addEventListener("click", () => enrollCourse(button.dataset.courseId));
        });
    } catch (error) {
        console.error("Error loading courses:", error);
        showError("Failed to load courses");
    }
}

async function enrollCourse(courseId) {
    try {
        await api.enrollCourse(courseId);
        showSuccess("Enrolled successfully!");
    } catch (error) {
        console.error("Error enrolling in course:", error);
        showError(error.message || "Failed to enroll in course");
    }
}

function showError(message) {
    alert(message);
}

function showSuccess(message) {
    alert(message);
}
