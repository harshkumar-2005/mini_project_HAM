import api from "./api.js";

async function checkAuth() {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "/login.html";
        return;
    }

    const userRole = localStorage.getItem("userRole");
    if (!userRole) {
        logout();
    }
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("userRole");
    window.location.href = "/login.html";
}

async function refreshAuthToken() {
    try {
        const response = await fetch("http://127.0.0.1:5000/auth/refresh", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
        });
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem("token", data.token);
        } else {
            logout();
        }
    } catch (error) {
        logout();
    }
}


document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            try {
                const response = await api.login(email, password);
                
                // Store token & role in localStorage
                localStorage.setItem("token", response.token);
                localStorage.setItem("userRole", response.role);

                // Redirect based on role
                if (response.role === "admin") {
                    window.location.href = "/admin.html";
                } else {
                    window.location.href = "/student.html";
                }
            } catch (error) {
                alert("Login failed: " + error.message);
            }
        });
    }

    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", logout);
    }
});

export { checkAuth, logout };
