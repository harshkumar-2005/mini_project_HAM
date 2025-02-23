import React, { useState } from 'react';

const EnrollmentForm = ({ onEnroll }) => {
    const [studentName, setStudentName] = useState("");
    
    const handleSubmit = (e) => {
        e.preventDefault();
        onEnroll(studentName);
    };
    
    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={studentName}
                onChange={(e) => setStudentName(e.target.value)}
                placeholder="Student Name"
            />
            <button type="submit">Enroll</button>
        </form>
    );
};

export default EnrollmentForm;
