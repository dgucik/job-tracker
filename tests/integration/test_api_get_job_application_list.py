import pytest


@pytest.mark.integration
async def test_returns_empty_list_when_no_applications(client):
    response = await client.get("/v1/job-applications/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.integration
async def test_returns_multiple_applications(client):
    await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Company 0",
            "roleName": "Role 0",
            "postingUrl": "https://company0.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
        },
    )
    await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Company 1",
            "roleName": "Role 1",
            "postingUrl": "https://company1.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
        },
    )
    await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Company 2",
            "roleName": "Role 2",
            "postingUrl": "https://company2.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
        },
    )

    response = await client.get("/v1/job-applications/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all("id" in app and "companyName" in app for app in data)


@pytest.mark.integration
async def test_returns_all_fields(client):
    create_resp = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Test Corp",
            "roleName": "Senior Dev",
            "postingUrl": "https://test.com/job",
            "status": "OFFERED",
            "workModel": "HYBRID",
            "workLocation": "Berlin",
            "compensations": [
                {
                    "minSalary": 8000,
                    "maxSalary": 12000,
                    "currency": "EUR",
                    "employmentType": "PERMANENT",
                }
            ],
            "notes": "Great benefits",
        },
    )
    assert create_resp.status_code == 201

    response = await client.get("/v1/job-applications/")
    assert response.status_code == 200
    app = response.json()[0]
    assert app["companyName"] == "Test Corp"
    assert app["roleName"] == "Senior Dev"
    assert app["postingUrl"] == "https://test.com/job"
    assert app["status"] == "OFFERED"
    assert app["workModel"] == "HYBRID"
    assert app["workLocation"] == "Berlin"
    assert app["notes"] == "Great benefits"
    assert len(app["compensations"]) == 1
    assert app["compensations"][0]["minSalary"] == 8000


@pytest.mark.integration
async def test_returns_null_optional_fields(client):
    await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Minimal Corp",
            "roleName": "Dev",
            "postingUrl": "https://min.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
            "workLocation": None,
            "compensations": [],
            "notes": None,
        },
    )

    response = await client.get("/v1/job-applications/")
    assert response.status_code == 200
    app = response.json()[0]
    assert app["workLocation"] is None
    assert app["notes"] is None
    assert app["compensations"] == []


@pytest.mark.integration
async def test_returns_multiple_compensations(client):
    await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Multi Corp",
            "roleName": "Consultant",
            "postingUrl": "https://multi.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
            "compensations": [
                {
                    "minSalary": 5000,
                    "maxSalary": 7000,
                    "currency": "PLN",
                    "employmentType": "B2B",
                },
                {
                    "minSalary": 4000,
                    "maxSalary": 6000,
                    "currency": "PLN",
                    "employmentType": "PERMANENT",
                },
            ],
        },
    )

    response = await client.get("/v1/job-applications/")
    assert response.status_code == 200
    app = response.json()[0]
    assert len(app["compensations"]) == 2
