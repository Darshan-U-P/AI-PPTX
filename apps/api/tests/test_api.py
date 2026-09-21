def test_presentation_and_slide_crud(client):
    created = client.post("/api/v1/presentations", json={"title": "Demo"})
    assert created.status_code == 201
    presentation = created.json()
    presentation_id = presentation["id"]
    assert client.get(f"/api/v1/presentations/{presentation_id}").json()["metadata"]["title"] == "Demo"
    assert client.patch(f"/api/v1/presentations/{presentation_id}", json={"title": "Updated"}).json()["metadata"]["title"] == "Updated"
    slide = client.post(f"/api/v1/presentations/{presentation_id}/slides", json={"elements": []})
    assert slide.status_code == 201
    slide_id = slide.json()["id"]
    update = client.patch(f"/api/v1/slides/{slide_id}", json={"elements": [{"type": "text", "x": 1, "y": 1, "width": 4, "height": 1, "text": "Editable"}]})
    assert update.status_code == 200
    assert update.json()["elements"][0]["text"] == "Editable"
    assert client.delete(f"/api/v1/slides/{slide_id}").status_code == 204


def test_invalid_slide_payload_returns_consistent_validation_error(client):
    presentation_id = client.post("/api/v1/presentations", json={"title": "Demo"}).json()["id"]
    response = client.post(f"/api/v1/presentations/{presentation_id}/slides", json={"elements": [{"type": "text", "x": -1, "y": 0, "width": 1, "height": 1, "text": "bad"}]})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_local_ai_status_reports_unavailable_local_service(client):
    response = client.get("/api/v1/ai/status")
    assert response.status_code == 200
    assert response.json()["provider"] == "localai"
    assert response.json()["base_url"].startswith("http://localhost")
