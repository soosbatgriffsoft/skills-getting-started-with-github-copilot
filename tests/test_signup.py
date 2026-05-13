"""
Tests for the signup endpoint (POST /activities/{activity_name}/signup).
"""

import pytest


def test_signup_new_participant_adds_to_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    activities_response = client.get("/activities")
    activities_data = activities_response.json()

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert email in activities_data[activity_name]["participants"]


def test_signup_activity_not_found_returns_404(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    assert "already" in response.json()["detail"].lower()


def test_signup_multiple_activities_for_same_student(client):
    # Arrange
    email = "multistudent@mergington.edu"

    # Act
    response_1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    response_2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": email}
    )
    activities_data = client.get("/activities").json()

    # Assert
    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert email in activities_data["Chess Club"]["participants"]
    assert email in activities_data["Programming Class"]["participants"]


@pytest.mark.parametrize(
    "activity_name,email",
    [
        ("Basketball Team", "basketball@mergington.edu"),
        ("Art Studio", "artist@mergington.edu"),
        ("Debate Team", "debater@mergington.edu"),
    ]
)
def test_signup_parametrized(client, activity_name, email):
    # Arrange

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    activities_data = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert email in activities_data[activity_name]["participants"]
