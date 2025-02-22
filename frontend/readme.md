frontend/
│── public/                  # Static assets
│   ├── index.html           # Main HTML template
│   ├── favicon.ico          # App icon
│── src/                     # React source files
│   ├── components/          # Reusable UI components
│   │   ├── Navbar.js        # Navigation bar
│   │   ├── CourseList.js    # Display available courses
│   │   ├── EnrollmentForm.js # Enroll in courses
│   │   ├── BulkEnroll.js    # Bulk enrollment feature
│   │   ├── Login.js         # User authentication form
│   ├── pages/               # Page-based components
│   │   ├── Home.js          # Home page
│   │   ├── AdminDashboard.js # Admin panel
│   │   ├── StudentDashboard.js # Student dashboard
│   ├── services/            # API calls to Flask backend
│   │   ├── api.js           # Axios functions for API requests
│   ├── context/             # Global state management
│   │   ├── AuthContext.js   # Authentication state
│   ├── App.js               # Main app component
│   ├── index.js             # React entry point
│── package.json             # Dependencies and scripts
│── .env                     # API URL and environment variables
│── README.md                # Project setup instructions
