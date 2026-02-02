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
async def test_updates_status_successfully(client, created_application):
    response = await client.put(
        f"/v1/job-applications/{created_application}/status",
        json={"status": "INTERVIEWED"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == created_application


@pytest.mark.integration
async def test_persists_status_in_database(client, created_application):
    await client.put(
        f"/v1/job-applications/{created_application}/status",
        json={"status": "OFFERED"},
    )

    list_resp = await client.get("/v1/job-applications/")
    app = next(a for a in list_resp.json() if a["id"] == created_application)
    assert app["status"] == "OFFERED"


@pytest.mark.integration
async def test_returns_404_for_non_existent_application(client):
    non_existent_id = str(uuid4())
    response = await client.put(
        f"/v1/job-applications/{non_existent_id}/status",
        json={"status": "INTERVIEWED"},
    )
    assert response.status_code == 404


@pytest.mark.integration
async def test_returns_422_for_invalid_uuid(client):
    response = await client.put(
        "/v1/job-applications/not-a-uuid/status",
        json={"status": "INTERVIEWED"},
    )
    assert response.status_code == 422


@pytest.mark.integration
async def test_returns_422_for_invalid_status(client, created_application):
    response = await client.put(
        f"/v1/job-applications/{created_application}/status",
        json={"status": "INVALID_STATUS"},
    )
    assert response.status_code == 422


@pytest.mark.integration
async def test_returns_422_when_status_missing(client, created_application):
    response = await client.put(
        f"/v1/job-applications/{created_application}/status",
        json={},
    )
    assert response.status_code == 422


@pytest.mark.integration
async def test_returns_422_when_status_null(client, created_application):
    response = await client.put(
        f"/v1/job-applications/{created_application}/status",
        json={"status": None},
    )
    assert response.status_code == 422


@pytest.mark.integration
@pytest.mark.parametrize(
    "status_value", ["APPLIED", "INTERVIEWED", "OFFERED", "ACCEPTED", "REJECTED"]
)
async def test_succeeds_for_status_values(client, created_application, status_value):
    response = await client.put(
        f"/v1/job-applications/{created_application}/status",
        json={"status": status_value},
    )
    assert response.status_code == 200


@pytest.mark.integration
async def test_succeeds_updating_to_same_status(client, created_application):
    response = await client.put(
        f"/v1/job-applications/{created_application}/status",
        json={"status": "APPLIED"},
    )
    assert response.status_code == 200


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
        f"/v1/job-applications/{app_id}/status",
        json={"status": "INTERVIEWED"},
    )

    list_resp = await client.get("/v1/job-applications/")
    app = next(a for a in list_resp.json() if a["id"] == app_id)
    assert app["status"] == "INTERVIEWED"
    assert app["companyName"] == "Test Corp"
    assert app["roleName"] == "Senior Dev"
    assert app["workLocation"] == "Warsaw"
    assert app["notes"] == "Original notes"
    assert len(app["compensations"]) == 1


@pytest.mark.integration
async def test_allows_multiple_status_updates(client, created_application):
    await client.put(
        f"/v1/job-applications/{created_application}/status",
        json={"status": "INTERVIEWED"},
    )
    await client.put(
        f"/v1/job-applications/{created_application}/status",
        json={"status": "OFFERED"},
    )
    await client.put(
        f"/v1/job-applications/{created_application}/status",
        json={"status": "ACCEPTED"},
    )

    list_resp = await client.get("/v1/job-applications/")
    app = next(a for a in list_resp.json() if a["id"] == created_application)
    assert app["status"] == "ACCEPTED"


@pytest.mark.integration
async def test_returns_422_for_lowercase_status(client, created_application):
    response = await client.put(
        f"/v1/job-applications/{created_application}/status",
        json={"status": "interviewed"},
    )
    assert response.status_code == 422
