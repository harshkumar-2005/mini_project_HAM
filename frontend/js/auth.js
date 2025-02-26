function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login.html';
        return;
    }

    // Validate token by calling a protected route
    api.getCourses()
        .then(() => {
            console.log('Token is valid');
        })
        .catch(() => {
            console.warn('Invalid or expired token. Redirecting to login...');
            localStorage.removeItem('token');
            window.location.href = '/login.html';
        });
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/login.html';
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const logoutBtn = document.getElementById('logoutBtn');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await api.login(email, password);
                localStorage.setItem('token', response.token);
                window.location.href = response.role === 'admin' ? '/admin.html' : '/student.html';
            } catch (error) {
                alert('Login failed: ' + error.message);
            }
        });
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const passwordToggle = document.querySelector('.password-toggle');
    const passwordInput = document.querySelector('#password');

    if (passwordToggle && passwordInput) {
        passwordToggle.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            // Toggle icon
            const icon = this.querySelector('i');
            icon.classList.toggle('fa-eye');
            icon.classList.toggle('fa-eye-slash');
        });
    }
});
