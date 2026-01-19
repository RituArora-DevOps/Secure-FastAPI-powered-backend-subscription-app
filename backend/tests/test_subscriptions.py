# Testing data logic (1 month/12-month calculations)

def test_subscription_duration_logic(client, admin_token, user_token):
    # 1. Admin creates a 3-month plan
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post("/plans/", headers=admin_headers, json = {
        "name": "Quaterly",
        "price": 19.99,
        "duration_months": 3
        })
    plan_data = response.json()
    plan_id = plan_data["id"]
    # 2. User subscribe
    user_header = {"Authorization": f"Bearer {user_token}"}
    sub_res = client.post("/subscriptions/",
                           headers=user_header, 
                           json={"plan_id": plan_id})
    
    assert sub_res.status_code == 200
    data = sub_res.json()

    #3. Verify math: end_date should be ~90 days after start_date
    from datetime import datetime
    start = datetime.fromisoformat(data["start_date"].replace("Z", "+00:00"))
    end = datetime.fromisoformat(data["end_date"].replace("Z", "+00:00"))
    diff_days = (end - start).days
    assert 89 <= diff_days <= 93 # Allowing for month length variations

def test_subscribe_to_invalid_plan(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    # Plan 999 does not exist
    response = client.post("/subscriptions/",
                           headers=headers, 
                           json={"plan_id": 999})
    assert response.status_code == 404
    assert response.json() == {"detail": "Invalid or inactive plan selected"}

def test_cancel_subscription_success(client, admin_token, user_token):
    # 1. Setup: Admin creates plan, User subscribes
    headers_a = {"Authorization": f"Bearer {admin_token}"}
    plan = client.post("/plans/", headers=headers_a, json={
        "name": "Monthly", "price": 9.99, "duration_months": 1
    }).json()
    
    headers_u = {"Authorization": f"Bearer {user_token}"}
    sub = client.post("/subscriptions/", headers=headers_u, json={"plan_id": plan["id"]}).json()
    
    # 2. Action: Cancel the subscription
    # Note: Ensure route is @router.patch("/{subscription_id}/cancel")
    response = client.patch(f"/subscriptions/{sub['id']}/cancel", headers=headers_u)
    
    assert response.status_code == 200
    assert response.json()["is_active"] is False

def test_prevent_duplicate_active_subscription(client, admin_token, user_token):
    # 1. Setup: User already has an active subscription
    headers_a = {"Authorization": f"Bearer {admin_token}"}
    plan = client.post("/plans/", headers=headers_a, json={"name": "Pro", "price": 20, "duration_months": 1}).json()
    
    headers_u = {"Authorization": f"Bearer {user_token}"}
    client.post("/subscriptions/", headers=headers_u, json={"plan_id": plan["id"]})
    
    # 2. Action: Subscribe to the same plan AGAIN
    response = client.post("/subscriptions/", headers=headers_u, json={"plan_id": plan["id"]})
    
    # 3. Assert: Should return 400 Bad Request
    assert response.status_code == 400
    assert "already has an active subscription" in response.json()["detail"]

def test_user_forbidden_from_viewing_others_sub(client, user_token, db_session, admin_token):
    from app.database.models.subscription import Subscription
    
    # 1. We need a valid Plan ID first (using admin_token to create it)
    headers_a = {"Authorization": f"Bearer {admin_token}"}
    plan = client.post("/plans/", headers=headers_a, json={
        "name": "Hidden Plan", "price": 50, "duration_months": 1
    }).json()

    # 2. Create another user manually to be the 'victim'
    from app.database.models.user import User
    victim = User(email="victim@test.com", name="Victim", hashed_password="...", is_admin=False)
    db_session.add(victim)
    db_session.commit()

    # 3. Create a subscription belonging to the victim
    other_sub = Subscription(user_id=victim.id, plan_id=plan["id"], is_active=True)
    db_session.add(other_sub)
    db_session.commit()

    # 4. Try to view it as the 'user_token' user
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get(f"/subscriptions/{other_sub.id}", headers=headers)
    
    # This hits the 'Forbidden' branch (Line 54-62 in your routes)
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"

def test_admin_read_all_subscriptions(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/subscriptions/all", headers=headers)
    assert response.status_code == 200