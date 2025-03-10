import api from "./api.js";
import { checkAuth, logout } from "./auth.js";

document.addEventListener("DOMContentLoaded", async () => {
    await checkAuth();
    const userRole = localStorage.getItem("userRole");

    // Redirect if user is not a student
    if (userRole !== "student") {
        showError("Unauthorized Access");
        setTimeout(() => {
            window.location.href = "/index.html";
        }, 2000);
        return;
    }

    // Load courses and set up event listeners
    await loadCourses();
    document.getElementById("logoutBtn").addEventListener("click", logout);
});

// Function to load available courses
async function loadCourses() {
    try {
        const courses = await api.getCourses();
        const coursesList = document.getElementById("coursesList");

        if (!courses.length) {
            coursesList.innerHTML = '<div class="empty-state">No courses available</div>';
            return;
        }

        // Render courses
        coursesList.innerHTML = courses.map(course => `
            <div class="course-card">
                <h3>${course.name}</h3>
                <p>${course.description || "No description available"}</p>
                <button class="enroll-btn" data-course-id="${course.id}">Enroll</button>
            </div>
        `).join("");

        // Add event listeners to enroll buttons
        document.querySelectorAll(".enroll-btn").forEach(button => {
            button.addEventListener("click", async () => {
                const courseId = button.dataset.courseId;
                await enrollCourse(courseId, button);
            });
        });
    } catch (error) {
        console.error("Error loading courses:", error);
        showError("Failed to load courses. Please try again later.");
    }
}

// Function to enroll in a course
async function enrollCourse(courseId, button) {
    try {
        // Disable the button to prevent multiple clicks
        button.disabled = true;
        button.textContent = "Enrolling...";

        // Enroll in the course
        await api.enrollCourse(courseId);

        // Update the button state
        button.textContent = "Enrolled";
        button.disabled = true;

        // Show success notification
        showSuccess("Enrolled successfully!");

        // Refresh the course list
        await loadCourses();
    } catch (error) {
        console.error("Error enrolling in course:", error);
        showError(error.message || "Failed to enroll in course");

        // Re-enable the button if enrollment fails
        button.disabled = false;
        button.textContent = "Enroll";
    }
}

// Function to show error notifications
function showError(message) {
    const notification = document.getElementById("notification");
    notification.textContent = message;
    notification.className = "notification error";
    notification.style.display = "block";

    setTimeout(() => {
        notification.style.display = "none";
    }, 3000);
}

// Function to show success notifications
function showSuccess(message) {
    const notification = document.getElementById("notification");
    notification.textContent = message;
    notification.className = "notification success";
    notification.style.display = "block";

    setTimeout(() => {
        notification.style.display = "none";
    }, 3000);
}