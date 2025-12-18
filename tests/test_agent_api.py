import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from agent.api import app

client = TestClient(app)

@pytest.fixture
def mock_executor():
    with patch("agent.api.shutdown") as mock_shutdown, \
         patch("agent.api.update_system") as mock_update, \
         patch("agent.api.list_installed_packages") as mock_packages:
        yield {
            "shutdown": mock_shutdown,
            "update": mock_update,
            "packages": mock_packages
        }

def test_handle_command_power_off(mock_executor):
    response = client.post("/agent/commands", json={"action": "POWER_OFF"})
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "Shutdown initiated"
    mock_executor["shutdown"].assert_called_once()

def test_handle_command_update(mock_executor):
    response = client.post("/agent/commands", json={"action": "UPDATE"})
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "Update initiated"
    mock_executor["update"].assert_called_once()

def test_handle_command_scan(mock_executor):
    mock_executor["packages"].return_value = [{"name": "test-pkg", "version": "1.0"}]
    response = client.post("/agent/commands", json={"action": "SCAN"})
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "details" in response.json()
    assert response.json()["details"]["packages_count"] == 1
    mock_executor["packages"].assert_called_once()

def test_handle_unknown_command():
    response = client.post("/agent/commands", json={"action": "INVALID_CMD"})
    assert response.status_code == 200
    assert response.json()["success"] is False
    assert "Unknown action" in response.json()["errorMessage"]

def test_handle_command_exception(mock_executor):
    mock_executor["shutdown"].side_effect = Exception("System Error")
    response = client.post("/agent/commands", json={"action": "POWER_OFF"})
    assert response.status_code == 200
    assert response.json()["success"] is False
    assert "System Error" in response.json()["errorMessage"]
