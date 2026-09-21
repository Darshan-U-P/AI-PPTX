def test_create_edit_validate_export_pipeline(client):
    presentation = client.post("/api/v1/presentations", json={"title": "Pipeline"}).json()
    slide = client.post(f"/api/v1/presentations/{presentation['id']}/slides", json={}).json()
    updated = client.patch(f"/api/v1/slides/{slide['id']}", json={"elements": [{"type": "text", "x": 1, "y": 1, "width": 5, "height": 1, "text": "Build with IR"}, {"type": "shape", "x": 1, "y": 2, "width": 3, "height": 1, "shape_type": "round_rect"}]} )
    assert updated.status_code == 200
    assert client.post(f"/api/v1/presentations/{presentation['id']}/validate").status_code == 200
    export = client.post(f"/api/v1/presentations/{presentation['id']}/export")
    assert export.status_code == 200
    assert export.headers["content-type"].startswith("application/vnd.openxmlformats-officedocument.presentationml.presentation")
    assert export.content.startswith(b"PK")
