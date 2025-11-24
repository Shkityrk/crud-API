"""
Locust load test for CRUD service (FastAPI)

How it works:
- Simulates users performing create/read/update/delete on /users endpoints
- Keeps created user IDs per simulated user and uses them for subsequent operations

Run locally (from project root `crud-py`):
1) Install locust: python -m pip install locust
2) Run UI: locust -f locustfile.py --host http://localhost:8080
   then open http://localhost:8089 in your browser
3) Or run headless smoke test: locust -f locustfile.py --headless -u 10 -r 2 --run-time 30s --host http://localhost:8080

Notes:
- The test attempts to be robust to different forms of returned id ("id", "_id", or Mongo-style {"$oid": "..."}).
- Adjust wait_time, task weights and host as needed.
"""

from __future__ import annotations

import random
import uuid
from typing import List, Optional

from locust import HttpUser, task, between


def _extract_id_from_response_json(obj: dict) -> Optional[str]:
    """Try to extract a sensible id string from various possible response shapes."""
    if not isinstance(obj, dict):
        return None
    # common fields
    if "id" in obj and obj["id"]:
        return str(obj["id"]) if not isinstance(obj["id"], dict) else _extract_id_from_response_json(obj["id"])
    if "_id" in obj and obj["_id"]:
        _id = obj["_id"]
        if isinstance(_id, dict) and "$oid" in _id:
            return str(_id["$oid"])
        return str(_id)
    # nested id like {'id': {'$oid': '...'}} or similar
    for k, v in obj.items():
        if isinstance(v, dict) and ("$oid" in v or "id" in v or "_id" in v):
            candidate = _extract_id_from_response_json(v)
            if candidate:
                return candidate
    return None


class CRUDUser(HttpUser):
    """Simulated user that performs CRUD operations on /users."""

    # pause between tasks
    wait_time = between(0.5, 1.5)

    def on_start(self):
        # store created user ids for this simulated user
        self.created_ids: List[str] = []

    @task(4)
    def create_user(self):
        """Create a new user (POST /users)"""
        unique = uuid.uuid4().hex[:8]
        payload = {
            "name": f"Load User {unique}",
            "email": f"load{unique}@example.com",
            "age": random.randint(18, 75),
        }
        with self.client.post("/users/", json=payload, catch_response=True) as response:
            if response.status_code == 201:
                try:
                    data = response.json()
                    user_id = _extract_id_from_response_json(data)
                    if user_id:
                        self.created_ids.append(user_id)
                        response.success()
                    else:
                        response.failure("created but no id found in response")
                except Exception as e:
                    response.failure(f"invalid json response: {e}")
            else:
                response.failure(f"unexpected status {response.status_code}")

    @task(2)
    def get_all_users(self):
        """GET /users/"""
        self.client.get("/users/")

    @task(2)
    def get_user_by_id(self):
        """GET /users/{id} — pick a previously created id if any"""
        if not self.created_ids:
            return
        user_id = random.choice(self.created_ids)
        self.client.get(f"/users/{user_id}")

    @task(1)
    def update_user(self):
        """PUT /users/{id} — partial update"""
        if not self.created_ids:
            return
        user_id = random.choice(self.created_ids)
        payload = {}
        # randomly choose a field to update
        if random.random() < 0.5:
            payload["name"] = f"Updated {uuid.uuid4().hex[:6]}"
        if random.random() < 0.3:
            payload["age"] = random.randint(18, 75)
        # if payload empty, set name
        if not payload:
            payload["name"] = f"Updated {uuid.uuid4().hex[:6]}"
        self.client.put(f"/users/{user_id}", json=payload)

    @task(1)
    def delete_user(self):
        """DELETE /users/{id} — remove one of created ids"""
        if not self.created_ids:
            return
        user_id = random.choice(self.created_ids)
        with self.client.delete(f"/users/{user_id}", catch_response=True) as response:
            if response.status_code in (200, 204):
                # remove id locally
                try:
                    self.created_ids.remove(user_id)
                except ValueError:
                    pass
                response.success()
            elif response.status_code == 404:
                # already deleted or never existed — remove locally as well
                try:
                    self.created_ids.remove(user_id)
                except ValueError:
                    pass
                response.success()
            else:
                response.failure(f"unexpected status {response.status_code}")


# Optional small helper for manual quick smoke run without Locust tooling
if __name__ == "__main__":
    print("This file is a Locust test scenario. Run it with Locust, e.g:\n  locust -f locustfile.py --host http://localhost:8080")
