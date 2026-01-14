# For verification the working of RBAC
def test_create_plan_as_admin(client, admin_token):
    response = client.post(
        "/plans/",
        json={
            "name": "Test Plan",
            "price": 9.99,
            "description": "This is a test plan",
            "duration_months": 12
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Plan"
    assert response.json()["price"] == 9.99

def test_create_plan_forbidden_for_user(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/plans/", headers=headers, json={
            "name": "Illegal Plan", "price": 0, "duration_months": 1
        })
    assert response.status_code == 403
    assert response.json() == {"detail": "The user does not have enough privileges"}

def test_get_single_plan(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    # Create it
    response = client.post("/plans/", headers=headers, json={
        "name": "single",
        "price": 9.9,
        "duration_months": 1
        })
    # Get it
    plan_id = response.json()["id"]
    response = client.get(f"/plans/{plan_id}", headers=headers)
    assert response.status_code == 200

def test_delete_plan(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    # Create it
    plan = client.post("/plans/", headers=headers, json={
        "name": "delete",
        "price": 9.9,
        "duration_months": 1
        }).json()
    # Delete it
    response = client.delete(f"/plans/{plan['id']}", headers=headers)
    assert response.status_code == 204

def test_cancel_subscription(client, user_token, admin_token):
    # 1. Setup a plan and subscription
    headers_a = {"Authorization": f"Bearer {admin_token}"}
    p = client.post("/plans/", headers=headers_a, json={"name":"Sub", "price":1, "duration_months":1}).json()
    
    headers_u = {"Authorization": f"Bearer {user_token}"}
    s = client.post("/subscriptions/", headers=headers_u, json={"plan_id": p['id']}).json()
    
    # 2. Cancel it
    res = client.patch(f"/subscriptions/{s['id']}/cancel", headers=headers_u)
    assert res.status_code == 200
    assert res.json()["is_active"] == False

def test_update_plan_success(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    # 1. Create a plan to update
    plan = client.post("/plans/", headers=headers, json={
        "name": "Old Plan", "price": 10.0, "duration_months": 1
    }).json()
    
    # 2. Update the plan
    response = client.put(f"/plans/{plan['id']}", headers=headers, json={
        "name": "Updated Plan Name",
        "price": 15.0
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Plan Name"
    assert response.json()["price"] == 15.0

def test_delete_plan_success(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    # 1. Create a plan to delete
    plan = client.post("/plans/", headers=headers, json={
        "name": "Delete Me", "price": 5.0, "duration_months": 1
    }).json()
    
    # 2. Delete it
    response = client.delete(f"/plans/{plan['id']}", headers=headers)
    assert response.status_code == 204
    
    # 3. Verify it's gone
    get_res = client.get(f"/plans/{plan['id']}")
    assert get_res.status_code == 404

def test_admin_get_plans_list(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/plans/", headers=headers)
    assert response.status_code == 200