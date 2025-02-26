import requests

BASE_URL = "http://127.0.0.1:5000"

def get_token():
    """Logs in as a test user and retrieves a JWT token."""
    login_data = {"email": "harsh@example.com", "password": "password123"}  # Ensure this user exists in DB
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if response.status_code == 200:
        return response.json().get("token")
    else:
        print("Login failed:", response.text)
        return None

def test_enroll_student():
    """Attempts to enroll a student in a course."""
    token = get_token()
    if not token:
        print("Token retrieval failed. Cannot proceed with enrollment test.")
        return

    headers = {"Authorization": f"Bearer {token}"}
    data = {"course_id": 1}  # Ensure this course exists in DB

    response = requests.post(f"{BASE_URL}/enroll", json=data, headers=headers)

    # Debugging Output
    print("Response Code:", response.status_code)
    print("Response Content:", response.text)

    assert response.status_code in [200, 201], "Enrollment failed"

if __name__ == "__main__":
    test_enroll_student()
