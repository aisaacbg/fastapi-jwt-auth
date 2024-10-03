import time
from jose import jwt
from app.config import settings

def test_register_user(client):
    timestamp = str(int(time.time()))
    response = client.post("/register", json={
        "username": f"testuser_{timestamp}",
        "email": f"testuser_{timestamp}@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 200
    assert response.json()["email"] == f"testuser_{timestamp}@example.com"
    assert response.json()["username"] == f"testuser_{timestamp}"

def test_login_user(client):
    timestamp = str(int(time.time()))
    
    # Register a new user
    client.post("/register", json={
        "username": f"testuser_{timestamp}",
        "email": f"testuser_{timestamp}@example.com",
        "password": "password123"
    })
    
    # Attempt to log in with the same user
    response = client.post("/login", data={
        "username": f"testuser_{timestamp}",
        "password": "password123"
    })

    print(response.json())  # Debugging print
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_refresh_token(client):
    timestamp = str(int(time.time()))
    
    # Register and log in a user
    client.post("/register", json={
        "username": f"testuser_{timestamp}",
        "email": f"testuser_{timestamp}@example.com",
        "password": "password123"
    })
    
    login_response = client.post("/login", data={
        "username": f"testuser_{timestamp}",
        "password": "password123"
    })
    
    token = login_response.json()["access_token"]
    
    # Use the token to refresh
    refresh_response = client.post("/token/refresh", headers={"Authorization": f"Bearer {token}"})
    
    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json()

def test_verify_token(client):
    timestamp = str(int(time.time()))

    # Register and log in a user
    client.post("/register", json={
        "username": f"testuser_{timestamp}",
        "email": f"testuser_{timestamp}@example.com",
        "password": "password123"
    })

    login_response = client.post("/login", data={
        "username": f"testuser_{timestamp}",
        "password": "password123"
    })

    token = login_response.json()["access_token"]

    # Verify the token by sending it in the Authorization header
    verify_response = client.post("/token/verify", headers={"Authorization": f"Bearer {token}"})

    assert verify_response.status_code == 200




def test_logout_user(client):
    timestamp = str(int(time.time()))
    
    # Register and log in a user
    client.post("/register", json={
        "username": f"testuser_{timestamp}",
        "email": f"testuser_{timestamp}@example.com",
        "password": "password123"
    })
    
    login_response = client.post("/login", data={
        "username": f"testuser_{timestamp}",
        "password": "password123"
    })
    
    token = login_response.json()["access_token"]
    
    # Perform logout
    logout_response = client.post("/logout", headers={"Authorization": f"Bearer {token}"})
    
    assert logout_response.status_code == 200
    assert logout_response.json()["msg"] == "Logout successful"

