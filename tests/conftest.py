"""
Pytest configuration and shared fixtures for API tests.
"""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture(scope="session")
def client():
    """Provide a reusable TestClient for the FastAPI app."""
    return TestClient(app)


ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Reset the in-memory activities state before each test."""
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    yield
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
