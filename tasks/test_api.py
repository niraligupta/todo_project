import json
import pytest
from django.test import Client
from tasks import db
import importlib

@pytest.fixture(autouse=True)
def reset_db(tmp_path, monkeypatch):
    from django.conf import settings
    test_db = tmp_path / "test_db.sqlite3"
    settings.DATABASES['default']['NAME'] = str(test_db)

    importlib.reload(db)
    db.init_db_if_needed()
    yield


def test_create_and_get_task():
    client = Client()
    payload = {"title": "Buy groceries", "description": "Milk, Eggs", "due_date": "2025-12-31"}
    resp = client.post("/api/tasks/", json.dumps(payload), content_type="application/json")
    assert resp.status_code == 201
    data = resp.json()
    assert "task" in data
    tid = data["task"]["id"]

    resp2 = client.get(f"/api/tasks/{tid}/")
    assert resp2.status_code == 200
    d2 = resp2.json()
    assert d2["task"]["title"] == "Buy groceries"

def test_update_task():
    client = Client()
    payload = {"title": "Task 1"}
    resp = client.post("/api/tasks/", json.dumps(payload), content_type="application/json")
    tid = resp.json()["task"]["id"]

    upd = {"description": "Updated description", "status": "done"}
    resp2 = client.put(f"/api/tasks/{tid}/", json.dumps(upd), content_type="application/json")
    assert resp2.status_code == 200
    assert resp2.json()["task"]["status"] == "done"
    assert resp2.json()["task"]["description"] == "Updated description"

def test_delete_task():
    client = Client()
    resp = client.post("/api/tasks/", json.dumps({"title": "To be deleted"}), content_type="application/json")
    tid = resp.json()["task"]["id"]

    delr = client.delete(f"/api/tasks/{tid}/")
    assert delr.status_code == 200
    assert client.get(f"/api/tasks/{tid}/").status_code == 404

def test_list_tasks():
    client = Client()
    for i in range(3):
        client.post("/api/tasks/", json.dumps({"title": f"t{i}"}), content_type="application/json")
    r = client.get("/api/tasks/")
    assert r.status_code == 200
    tasks = r.json()["tasks"]
    assert len(tasks) >= 3
