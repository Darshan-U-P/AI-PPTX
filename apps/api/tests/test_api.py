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
    assert client.delete(f"/api/v1/presentations/{presentation_id}").status_code == 204


def test_health_listing_order_and_image_upload(client, tmp_path):
    assert client.get("/health").json() == {"status": "ok"}
    presentation = client.post("/api/v1/presentations", json={"title": "Assets"}).json()
    assert len(client.get("/api/v1/presentations").json()) == 1
    first = client.post(f"/api/v1/presentations/{presentation['id']}/slides", json={}).json()
    second = client.post(f"/api/v1/presentations/{presentation['id']}/slides", json={}).json()
    client.patch(f"/api/v1/slides/{second['id']}", json={"order": 0})
    ordered = client.get(f"/api/v1/presentations/{presentation['id']}/slides").json()
    assert [slide["id"] for slide in ordered] == [second["id"], first["id"]]
    image = tmp_path / "asset.png"
    image.write_bytes(b"\x89PNG\r\n\x1a\n")
    upload = client.post(f"/api/v1/presentations/{presentation['id']}/assets", files={"file": ("asset.png", image.read_bytes(), "image/png")}, data={"alt": "Sample"})
    assert upload.status_code == 201
    asset = upload.json()
    assert client.get(f"/api/v1/assets/{asset['id']}").status_code == 200


def test_invalid_slide_payload_returns_consistent_validation_error(client):
    presentation_id = client.post("/api/v1/presentations", json={"title": "Demo"}).json()["id"]
    response = client.post(f"/api/v1/presentations/{presentation_id}/slides", json={"elements": [{"type": "text", "x": -1, "y": 0, "width": 1, "height": 1, "text": "bad"}]})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_local_ai_status_reports_unavailable_local_service(client):
    response = client.get("/api/v1/ai/status")
    assert response.status_code == 200
    assert response.json()["provider"] == "local"
    assert response.json()["available"] is False
    assert response.json()["base_url"].startswith("http://localhost")
