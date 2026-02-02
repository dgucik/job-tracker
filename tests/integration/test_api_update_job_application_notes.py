import pytest
from uuid import uuid4


@pytest.fixture
async def created_application(client):
    create_resp = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Test Corp",
            "roleName": "Developer",
            "postingUrl": "https://test.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
        },
    )
    return create_resp.json()["id"]


@pytest.mark.integration
async def test_updates_notes_successfully(client, created_application):
    response = await client.put(
        f"/v1/job-applications/{created_application}/notes",
        json={"notes": "Updated notes content"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == created_application


@pytest.mark.integration
async def test_persists_notes_in_database(client, created_application):
    new_notes = "These are the updated notes"
    await client.put(
        f"/v1/job-applications/{created_application}/notes",
        json={"notes": new_notes},
    )

    list_resp = await client.get("/v1/job-applications/")
    app = next(a for a in list_resp.json() if a["id"] == created_application)
    assert app["notes"] == new_notes


@pytest.mark.integration
async def test_returns_404_for_non_existent_application(client):
    non_existent_id = str(uuid4())
    response = await client.put(
        f"/v1/job-applications/{non_existent_id}/notes",
        json={"notes": "Some notes"},
    )
    assert response.status_code == 404


@pytest.mark.integration
async def test_returns_422_for_invalid_uuid(client):
    response = await client.put(
        "/v1/job-applications/not-a-uuid/notes",
        json={"notes": "Some notes"},
    )
    assert response.status_code == 422


@pytest.mark.integration
async def test_succeeds_with_empty_string(client, created_application):
    response = await client.put(
        f"/v1/job-applications/{created_application}/notes",
        json={"notes": ""},
    )
    assert response.status_code == 200


@pytest.mark.integration
async def test_succeeds_with_special_characters(client, created_application):
    special_notes = 'Notes with special chars: @#$%^&*()_+-={}[]|\\:";<>?,./~`\n\t'
    response = await client.put(
        f"/v1/job-applications/{created_application}/notes",
        json={"notes": special_notes},
    )
    assert response.status_code == 200

    list_resp = await client.get("/v1/job-applications/")
    app = next(a for a in list_resp.json() if a["id"] == created_application)
    assert app["notes"] == special_notes


@pytest.mark.integration
async def test_succeeds_with_unicode(client, created_application):
    unicode_notes = "Notes with unicode: 你好 مرحبا שלום ñ ü ö"
    response = await client.put(
        f"/v1/job-applications/{created_application}/notes",
        json={"notes": unicode_notes},
    )
    assert response.status_code == 200

    list_resp = await client.get("/v1/job-applications/")
    app = next(a for a in list_resp.json() if a["id"] == created_application)
    assert app["notes"] == unicode_notes


@pytest.mark.integration
async def test_returns_422_when_notes_missing(client, created_application):
    response = await client.put(
        f"/v1/job-applications/{created_application}/notes",
        json={},
    )
    assert response.status_code == 422


@pytest.mark.integration
async def test_returns_422_when_notes_null(client, created_application):
    response = await client.put(
        f"/v1/job-applications/{created_application}/notes",
        json={"notes": None},
    )
    assert response.status_code == 422


@pytest.mark.integration
async def test_does_not_affect_other_fields(client):
    create_resp = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Test Corp",
            "roleName": "Senior Dev",
            "postingUrl": "https://test.com",
            "status": "APPLIED",
            "workModel": "HYBRID",
            "workLocation": "Warsaw",
            "compensations": [
                {
                    "minSalary": 5000,
                    "maxSalary": 8000,
                    "currency": "PLN",
                    "employmentType": "B2B",
                }
            ],
            "notes": "Original notes",
        },
    )
    app_id = create_resp.json()["id"]

    await client.put(
        f"/v1/job-applications/{app_id}/notes",
        json={"notes": "Updated notes"},
    )

    list_resp = await client.get("/v1/job-applications/")
    app = next(a for a in list_resp.json() if a["id"] == app_id)
    assert app["notes"] == "Updated notes"
    assert app["companyName"] == "Test Corp"
    assert app["status"] == "APPLIED"
    assert app["workLocation"] == "Warsaw"
    assert len(app["compensations"]) == 1


@pytest.mark.integration
async def test_allows_multiple_updates(client, created_application):
    await client.put(
        f"/v1/job-applications/{created_application}/notes",
        json={"notes": "First version"},
    )
    await client.put(
        f"/v1/job-applications/{created_application}/notes",
        json={"notes": "Second version"},
    )
    await client.put(
        f"/v1/job-applications/{created_application}/notes",
        json={"notes": "Final version"},
    )

    list_resp = await client.get("/v1/job-applications/")
    app = next(a for a in list_resp.json() if a["id"] == created_application)
    assert app["notes"] == "Final version"


@pytest.mark.integration
async def test_updates_from_null_to_value(client, created_application):
    list_resp = await client.get("/v1/job-applications/")
    app = next(a for a in list_resp.json() if a["id"] == created_application)
    assert app["notes"] is None

    response = await client.put(
        f"/v1/job-applications/{created_application}/notes",
        json={"notes": "Now with notes"},
    )
    assert response.status_code == 200

    list_resp = await client.get("/v1/job-applications/")
    app = next(a for a in list_resp.json() if a["id"] == created_application)
    assert app["notes"] == "Now with notes"


@pytest.mark.integration
async def test_succeeds_with_multiline_text(client, created_application):
    multiline_notes = "Line 1\nLine 2\nLine 3\n    Indented line"
    response = await client.put(
        f"/v1/job-applications/{created_application}/notes",
        json={"notes": multiline_notes},
    )
    assert response.status_code == 200

    list_resp = await client.get("/v1/job-applications/")
    app = next(a for a in list_resp.json() if a["id"] == created_application)
    assert app["notes"] == multiline_notes
