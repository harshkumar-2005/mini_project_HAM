document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    loadCourses();

    document.getElementById('addCourseForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        await addCourse();
    });

    document.getElementById('logoutBtn').addEventListener('click', logout);
});

async function loadCourses() {
    try {
        const courses = await api.getCourses();
        const coursesList = document.getElementById('coursesList');

        if (!courses.length) {
            coursesList.innerHTML = '<div class="empty-state">No courses available</div>';
            return;
        }

        coursesList.innerHTML = courses.map(course => `
            <div class="course-card">
                <h3>${course.name}</h3>
                <p>${course.description || 'No description available'}</p>
                ${course.prerequisite_id ? `<p class="prerequisite">Prerequisite: Course ID ${course.prerequisite_id}</p>` : ''}
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading courses:', error);
        showError('Failed to load courses');
    }
}

async function addCourse() {
    const name = document.getElementById('courseName').value.trim();
    const description = document.getElementById('courseDescription').value.trim();
    const prerequisiteId = document.getElementById('prerequisiteId').value || null;

    if (!name) {
        showError('Course name is required');
        return;
    }

    try {
        await apiRequest('/add_course', {
            method: 'POST',
            body: JSON.stringify({
                name,
                description,
                prerequisite_id: prerequisiteId
            })
        });

        showSuccess('Course added successfully!');
        document.getElementById('addCourseForm').reset();
        await loadCourses();  // Refresh the course list
    } catch (error) {
        console.error('Error adding course:', error);
        showError(error.message || 'Failed to add course');
    }
}

function showError(message) {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = 'notification error';
    setTimeout(() => notification.className = 'notification', 3000);
}

function showSuccess(message) {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = 'notification success';
    setTimeout(() => notification.className = 'notification', 3000);
}
