import pytest
from uuid import uuid4


@pytest.mark.integration
async def test_deletes_existing_application(client):
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
    app_id = create_resp.json()["id"]

    response = await client.delete(f"/v1/job-applications/{app_id}")
    assert response.status_code == 204
    assert response.content == b""


@pytest.mark.integration
async def test_returns_404_for_non_existent_application(client):
    non_existent_id = str(uuid4())
    response = await client.delete(f"/v1/job-applications/{non_existent_id}")
    assert response.status_code == 404


@pytest.mark.integration
async def test_returns_422_for_invalid_uuid(client):
    response = await client.delete("/v1/job-applications/not-a-uuid")
    assert response.status_code == 422


@pytest.mark.integration
async def test_removes_application_from_database(client):
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
    app_id = create_resp.json()["id"]

    list_resp = await client.get("/v1/job-applications/")
    assert any(a["id"] == app_id for a in list_resp.json())

    await client.delete(f"/v1/job-applications/{app_id}")

    list_resp_after = await client.get("/v1/job-applications/")
    assert not any(a["id"] == app_id for a in list_resp_after.json())


@pytest.mark.integration
async def test_returns_404_on_second_delete(client):
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
    app_id = create_resp.json()["id"]

    first_delete = await client.delete(f"/v1/job-applications/{app_id}")
    assert first_delete.status_code == 204

    second_delete = await client.delete(f"/v1/job-applications/{app_id}")
    assert second_delete.status_code == 404


@pytest.mark.integration
async def test_deletes_application_with_compensations(client):
    create_resp = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Test Corp",
            "roleName": "Developer",
            "postingUrl": "https://test.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
            "compensations": [
                {
                    "minSalary": 5000,
                    "maxSalary": 8000,
                    "currency": "USD",
                    "employmentType": "B2B",
                },
                {
                    "minSalary": 4000,
                    "maxSalary": 6000,
                    "currency": "USD",
                    "employmentType": "PERMANENT",
                },
            ],
        },
    )
    app_id = create_resp.json()["id"]

    response = await client.delete(f"/v1/job-applications/{app_id}")
    assert response.status_code == 204


@pytest.mark.integration
async def test_does_not_affect_other_applications(client):
    create1 = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Corp A",
            "roleName": "Dev A",
            "postingUrl": "https://a.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
        },
    )
    create2 = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Corp B",
            "roleName": "Dev B",
            "postingUrl": "https://b.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
        },
    )
    app_id_1 = create1.json()["id"]
    app_id_2 = create2.json()["id"]

    await client.delete(f"/v1/job-applications/{app_id_1}")

    list_resp = await client.get("/v1/job-applications/")
    remaining = list_resp.json()
    assert any(a["id"] == app_id_2 for a in remaining)
    assert not any(a["id"] == app_id_1 for a in remaining)


@pytest.mark.integration
async def test_accepts_uppercase_uuid(client):
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
    app_id = create_resp.json()["id"]
    app_id_upper = app_id.upper()

    response = await client.delete(f"/v1/job-applications/{app_id_upper}")
    assert response.status_code == 204
