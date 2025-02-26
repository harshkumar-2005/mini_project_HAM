import pymysql

def test_db_connection():
    """Attempts to connect to the MySQL database and handles errors properly."""
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="@Harsh1243",
            database="student_course_reg",
            autocommit=True
        )
        print("✅ Database connection successful!")
    except pymysql.OperationalError as e:
        print(f"❌ Database connection failed: {e}")
    except pymysql.MySQLError as e:
        print(f"⚠️ MySQL error: {e}")
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()
            print("🔌 Database connection closed.")

if __name__ == "__main__":
    test_db_connection()
