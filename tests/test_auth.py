def test_login_wrong_password(client):
    # First create the user
    client.post("/users/", json={
        "email": "wrong@test.com",
        "name": "Test User",
        "password": "testpassword"
})
    # Try to logniwith wrong password
    response = client.post("/auth/login", data={
        "username": "wrong@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_login_user_not_found(client):
    # Try logging in with an email that doesn't exist
    response = client.post("/auth/login", data={
        "username": "ghost@test.com",
        "password": "password"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_access_protected_route_with_junk_token(client):
    headers = {"Authorization": "Bearer not-a-real-token"}
    response = client.get("/subscriptions/me", headers=headers)
    assert response.status_code == 401 # Unauthorized