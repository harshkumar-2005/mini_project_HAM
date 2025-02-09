import pymysql

# Connect to MySQL
conn = pymysql.connect(host="localhost", user="root", password="@Harsh1243", database="student_course_reg")
cursor = conn.cursor()

#  Ensure at least one student exists
cursor.execute("SELECT id FROM users WHERE role='student' LIMIT 1;")
student = cursor.fetchone()
if not student:
    cursor.execute("INSERT INTO users (name, email, role) VALUES ('harsh', 'harsh@example.com', 'student');")
    conn.commit()
    print("Added a default student.")
    cursor.execute("SELECT id FROM users WHERE role='student' LIMIT 1;")
    student = cursor.fetchone()

student_id = student[0]

#  Ensure at least one course exists
cursor.execute("SELECT id FROM courses LIMIT 1;")
course = cursor.fetchone()
if not course:
    cursor.execute("INSERT INTO courses (name, description) VALUES ('Python Basics', 'Intro to Python.');")
    conn.commit()
    print("Added a default course.")
    cursor.execute("SELECT id FROM courses LIMIT 1;")
    course = cursor.fetchone()

course_id = course[0]

print(f" Ready for testing: student_id={student_id}, course_id={course_id}")

cursor.close()
conn.close()
