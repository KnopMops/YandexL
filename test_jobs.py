from requests import delete, get, post

print("GET /api/v2/jobs")
print(get("http://localhost:5000/api/v2/jobs").json())

print("GET /api/v2/jobs/1")
print(get("http://localhost:5000/api/v2/jobs/1").json())
print("GET /api/v2/jobs/999")
print(get("http://localhost:5000/api/v2/jobs/999").json())

print("POST /api/v2/jobs (empty)")
print(post("http://localhost:5000/api/v2/jobs", json={}).json())
print("POST /api/v2/jobs (only job)")
print(post("http://localhost:5000/api/v2/jobs", json={"job": "Do something"}).json())

print("POST /api/v2/jobs (valid)")
print(
    post(
        "http://localhost:5000/api/v2/jobs",
        json={
            "team_leader": 1,
            "job": "Deployment of module 4",
            "work_size": 15,
            "collaborators": "2, 3",
            "is_finished": False,
        },
    ).json()
)

print("DELETE /api/v2/jobs/999")
print(delete("http://localhost:5000/api/v2/jobs/999").json())
