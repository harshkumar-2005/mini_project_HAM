import api from "./api.js";
import { checkAuth, logout } from "./auth.js";

document.addEventListener("DOMContentLoaded", async () => {
    await checkAuth();
    const userRole = localStorage.getItem("userRole");

    if (userRole !== "admin") {
        alert("Unauthorized Access");
        window.location.href = "/index.html";
        return;
    }

    loadCourses();

    document.getElementById("addCourseForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        await addCourse();
    });

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
                ${course.prerequisite_id ? `<p class="prerequisite">Prerequisite: Course ID ${course.prerequisite_id}</p>` : ""}
            </div>
        `).join("");
    } catch (error) {
        console.error("Error loading courses:", error);
        showError("Failed to load courses");
    }
}

async function addCourse() {
    const name = document.getElementById("courseName").value.trim();
    const description = document.getElementById("courseDescription").value.trim();
    const prerequisiteId = document.getElementById("prerequisiteId").value || null;

    if (!name) {
        showError("Course name is required");
        return;
    }

    try {
        await api.addCourse(name, description, prerequisiteId);
        showSuccess("Course added successfully!");
        document.getElementById("addCourseForm").reset();
        await loadCourses();
    } catch (error) {
        console.error("Error adding course:", error);
        showError(error.message || "Failed to add course");
    }
}

function showError(message) {
    alert(message);
}

function showSuccess(message) {
    alert(message);
}
