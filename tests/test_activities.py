"""
Tests for the activities listing endpoint (GET /activities).
"""


def test_get_all_activities_returns_all_items(client):
    # Arrange

    # Act
    response = client.get("/activities")
    activities_data = response.json()

    # Assert
    assert response.status_code == 200
    assert len(activities_data) == 9


def test_get_activities_response_contains_required_fields(client):
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    activities_data = response.json()

    # Assert
    assert response.status_code == 200
    for activity in activities_data.values():
        assert required_fields.issubset(activity.keys())
        assert isinstance(activity["participants"], list)
        assert isinstance(activity["max_participants"], int)


def test_get_activities_contains_expected_activity(client):
    # Arrange
    expected_activity_name = "Chess Club"

    # Act
    response = client.get("/activities")
    activities_data = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_activity_name in activities_data
    assert "michael@mergington.edu" in activities_data[expected_activity_name]["participants"]
