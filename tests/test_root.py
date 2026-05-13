"""
Tests for the root endpoint (GET /).
"""


def test_root_redirects_to_static(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert expected_location in response.headers["location"]


def test_root_follow_redirect_returns_200(client):
    # Arrange

    # Act
    response = client.get("/", follow_redirects=True)

    # Assert
    assert response.status_code == 200
