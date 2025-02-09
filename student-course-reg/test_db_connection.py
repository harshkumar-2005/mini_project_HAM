import pymysql

try:
    conn = pymysql.connect(host="localhost", user="root", password="@Harsh1243", database="student_course_reg")
    print(" Database connection successful!")
    conn.close()
except pymysql.MySQLError as e:
    print(f" Database connection failed: {e}")
