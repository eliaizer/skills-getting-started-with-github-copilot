import copy
from fastapi.testclient import TestClient
import pytest

from src import app as app_module


@pytest.fixture(autouse=True)
def restore_activities():
    # Make a deep copy of activities before each test and restore after
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = original


def test_get_activities():
    client = TestClient(app_module.app)
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect some known activities from the in-memory dataset
    assert "Programming Class" in data
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    client = TestClient(app_module.app)
    activity_name = "Programming Class"
    test_email = "test.user@example.com"

    # Ensure email not already present
    resp = client.get("/activities")
    assert resp.status_code == 200
    before = resp.json()[activity_name]["participants"]
    assert test_email not in before

    # Sign up
    resp = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert resp.status_code == 200
    json_body = resp.json()
    assert "Signed up" in json_body.get("message", "")

    # Verify participant added
    resp = client.get("/activities")
    after = resp.json()[activity_name]["participants"]
    assert test_email in after

    # Unregister
    resp = client.delete(f"/activities/{activity_name}/participants?email={test_email}")
    assert resp.status_code == 200
    json_body = resp.json()
    assert "Unregistered" in json_body.get("message", "")

    # Verify participant removed
    resp = client.get("/activities")
    final = resp.json()[activity_name]["participants"]
    assert test_email not in final
