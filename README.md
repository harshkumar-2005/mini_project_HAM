# Student Course Registration System 🎓

A simple **Student Course Registration System** built using **Flask** and **MySQL**.  
It supports **Role-Based Access Control (RBAC)** with authentication and **email notifications** for enrollment updates.  

### ✅ First Steps: 
```
   git clone https://github.com/harshkumar-2005/mini_project_HAM.git
```

---

## 📌 Features
✅ **User Authentication** (JWT/Flask-Login)  
✅ **Role-Based Access** (Admin & Student)  
✅ **Email Notifications** for enrollment updates  
✅ **MySQL Database Integration**  
✅ **REST API with CRUD operations**  

---

## 🚀 Getting Started

### 📂 Prerequisites
Make sure you have the following installed on your system:  
- **Python 3.12+**
- **MySQL**
- **Git**

---

## 📥 Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/mini_project_HAM.git
cd mini_project_HAM/student-course-reg/
```
### 2️⃣ Create a Virtual Environment
```sh
python -m venv venv
```
```sh
Windows: venv\Scripts\activate
```
```sh
macOS/Linux: source venv/bin/activate
```
### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```
### 4️⃣ Set Up Database
<ol>Create a .env file in the student-course-reg/ directory and add </ol>

```sh
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=student_course_db
```
<ol>Run the database setup script</ol>

```sh
python setup_db.py
```

### 5️⃣ Run Migrations

```sh
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
### 6️⃣ Start the Application

```sh
python app.py
```

<h2>The server should now be running on 
  
  ```sh
  http://127.0.0.1:5000/
```

<h3>You can test the API using Postman or the provided test_api.py script.</h3>

```sh
python test_api.py
```
<hr>
<h1>📂 Project Structure</h1>

```sh
mini_project_HAM/
│── student-course-reg/
│   │── app.py                # Main Flask application
│   │── auth_utils.py         # Authentication utilities
│   │── models.py             # Database models
│   │── routes.py             # API routes
│   │── setup_db.py           # Database setup script
│   │── test_api.py           # API testing script
│   │── test_db_connection.py # Database connection test
│   │── venv/                 # Virtual environment
│   │── migrations/           # Database migrations
│   └── requirements.txt      # Python dependencies
│── LICENSE
│── README.md
└── .gitignore
```

### 🤝 Contributing
<p>
  Contributions are welcome!
Feel free to open an issue or submit a pull request.
</p>

### 📜 License
<p>
  This project is licensed under the MIT License.
</p>

### 📧 Contact
<h6>For any questions, feel free to reach out. 😊</h6>

---





