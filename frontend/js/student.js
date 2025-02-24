document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    loadCourses();
    loadEnrollments();
});

async function loadCourses() {
    try {
        const courses = await api.getCourses();
        const coursesList = document.getElementById('coursesList');
        coursesList.innerHTML = courses.map(course => `
            <div class="course-card">
                <h3>${course.name}</h3>
                <p>${course.description}</p>
                <button onclick="enrollCourse(${course.id})" class="btn">Enroll</button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading courses:', error);
    }
}

async function loadEnrollments() {
    try {
        const enrollments = await api.getEnrollments();
        const enrollmentsList = document.getElementById('enrollmentsList');
        enrollmentsList.innerHTML = enrollments.map(enrollment => `
            <div class="enrollment-card">
                <h3>${enrollment.course.name}</h3>
                <p>Enrolled</p>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading enrollments:', error);
    }
}

async function enrollCourse(courseId) {
    try {
        await api.enrollCourse(courseId);
        loadEnrollments();
        alert('Successfully enrolled in course!');
    } catch (error) {
        alert('Failed to enroll: ' + error.message);
    }
}