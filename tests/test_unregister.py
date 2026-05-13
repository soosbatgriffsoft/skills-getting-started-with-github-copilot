"""
Tests for the unregister endpoint (DELETE /activities/{activity_name}/signup).
"""


def test_unregister_existing_participant_removes_them(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    activities_data = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    assert email not in activities_data[activity_name]["participants"]


def test_unregister_activity_not_found_returns_404(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_unregister_non_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "notfound@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_unregister_then_signup_again(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response_remove = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    response_add = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    activities_data = client.get("/activities").json()

    # Assert
    assert response_remove.status_code == 200
    assert response_add.status_code == 200
    assert email in activities_data[activity_name]["participants"]
