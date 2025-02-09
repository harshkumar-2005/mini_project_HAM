import requests

BASE_URL = "http://127.0.0.1:5000"

def test_enroll_student():
    data = {"student_id": 1, "course_id": 1}  # Make sure IDs exist in DB
    response = requests.post(f"{BASE_URL}/enroll", json=data)
    
    # Debugging Output
    print("Response Code:", response.status_code)
    print("Response Content:", response.text)

    assert response.status_code == 200  # Check if the request was successful

test_enroll_student()
