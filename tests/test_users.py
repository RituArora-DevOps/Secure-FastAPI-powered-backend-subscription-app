# --- POST TESTS ---
def test_create_user_success(client):
    # 1. Action: Send a POST request to our FastAPI route
    response = client.post("/users/", json={
            "email": "test_genai@exampples.com",
            "name": "Test User",
            "password": "testpassword"
        })
    
    # 2. Assert: Check if th status code is 201 (Created)
    assert response.status_code == 201

    # 3. Assert: Check if the returned data is correct
    data = response.json()
    assert data["email"] == "test_genai@exampples.com"
    assert "id" in data

def test_create_user_invalid_email(client):
    # Action: Send a request with a 'bad' email string
    response = client.post("/users/", json={
            "email": "not-an-email",
            "name": "Bad Test User",
            "password": "badpassword"
        })
    
    # Assert: Pydantic should catch this and return 422 (unprocessed entity)
    assert response.status_code == 422

# --- GET TESTS ---
def test_get_user_success(client):
    # First create a user to fetch
    user_in = {
        "email": "get@test.com",
        "name": "Test User",
        "password": "testpassword"
    }
    created = client.post("/users/", json=user_in).json()
    user_id = created["id"]

    # Now fetch them
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_in["email"]

def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

# --- PUT TESTS ---
def test_update_user_success(client):
    # First create a user to update
    user_in = {
        "email": "update@test.com",
        "name": "Test User",
        "password": "testpassword"
    }
    updated = client.post("/users/", json=user_in).json()
    user_id = updated["id"]

    # Now update
    updated_user = {
        "name": "Updated User"
    }
    response = client.put(f"/users/{user_id}", json=updated_user)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_user["name"]
    assert data["email"] == user_in["email"]

# --- DELETE TESTS ---
def test_delete_user_success(client):
    # 1. Create a user to update
    user_in = {
        "email": "update@test.com",
        "name": "Test User",
        "password": "testpassword"
    }
    updated = client.post("/users/", json=user_in).json()
    user_id = updated["id"]

    # 2. Delete
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204

    # 3. Verify they are gone
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "User not found"}