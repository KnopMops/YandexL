import requests

BASE_URL = "http://localhost:5000/api/jobs"

valid_job_data = {
    "team_leader": 1,
    "job": "Test job",
    "work_size": 10,
    "collaborators": "2,3",
    "start_date": "2025-01-01 10:00:00",
    "end_date": "2025-01-02 18:00:00",
    "is_finished": False,
}

invalid_job_data_missing_field = {
    "team_leader": 1,
    "job": "Test job",
    "work_size": 10,
    "collaborators": "2,3",
    "start_date": "2025-01-01 10:00:00",
    "is_finished": False,
}

invalid_job_data_wrong_type = {
    "team_leader": "not_int",
    "job": "Test job",
    "work_size": 10,
    "collaborators": "2,3",
    "start_date": "2025-01-01 10:00:00",
    "end_date": "2025-01-02 18:00:00",
    "is_finished": False,
}


def test_get_jobs_list():
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "jobs" in data, "Response should contain 'jobs' key"
    print("GET /api/jobs: OK")


def test_get_job_existing():
    job_id = 1
    response = requests.get(f"{BASE_URL}/{job_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "job" in data, "Response should contain 'job' key"
    print(f"GET /api/jobs/{job_id}: OK")


def test_get_job_not_found():
    job_id = 99999
    response = requests.get(f"{BASE_URL}/{job_id}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    data = response.json()
    assert "message" in data, "Response should contain error message"
    print(f"GET /api/jobs/{job_id} (not found): OK")


def test_create_job_valid():
    response = requests.post(BASE_URL, json=valid_job_data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "id" in data, "Response should contain created job id"
    job_id = data["id"]
    print(f"POST /api/jobs: created job with id {job_id}")
    delete_response = requests.delete(f"{BASE_URL}/{job_id}")
    assert delete_response.status_code == 200, (
        f"Failed to delete test job, status {delete_response.status_code}"
    )
    print(f"Deleted test job {job_id}")


def test_create_job_missing_field():
    response = requests.post(BASE_URL, json=invalid_job_data_missing_field)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    print("POST /api/jobs (missing field): OK")


def test_create_job_wrong_type():
    response = requests.post(BASE_URL, json=invalid_job_data_wrong_type)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    print("POST /api/jobs (wrong type): OK")


def test_delete_job_existing():
    create_response = requests.post(BASE_URL, json=valid_job_data)
    assert create_response.status_code == 200
    job_id = create_response.json()["id"]

    delete_response = requests.delete(f"{BASE_URL}/{job_id}")
    assert delete_response.status_code == 200, (
        f"Expected 200, got {delete_response.status_code}"
    )
    data = delete_response.json()
    assert "success" in data, "Response should contain 'success' key"
    print(f"DELETE /api/jobs/{job_id}: OK")

    get_response = requests.get(f"{BASE_URL}/{job_id}")
    assert get_response.status_code == 404, (
        f"Expected 404 after deletion, got {get_response.status_code}"
    )
    print(f"Confirmed job {job_id} is deleted")


def test_delete_job_not_found():
    job_id = 99999
    response = requests.delete(f"{BASE_URL}/{job_id}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    data = response.json()
    assert "message" in data, "Response should contain error message"
    print(f"DELETE /api/jobs/{job_id} (not found): OK")


if __name__ == "__main__":
    print("Starting API tests for Jobs...")
    test_get_jobs_list()
    test_get_job_existing()
    test_get_job_not_found()
    test_create_job_valid()
    test_create_job_missing_field()
    test_create_job_wrong_type()
    test_delete_job_existing()
    test_delete_job_not_found()
    print("All tests passed!")
