function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login.html';
        return;
    }

    api.getCourses()
        .then(() => console.log('Token is valid'))
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