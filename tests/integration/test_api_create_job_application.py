import pytest
from uuid import UUID


@pytest.mark.integration
async def test_creates_with_minimal_required_fields(client):
    response = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Min Corp",
            "roleName": "Dev",
            "postingUrl": "https://min.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert UUID(data["id"])


@pytest.mark.integration
async def test_creates_with_all_fields(client):
    response = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Full Corp",
            "roleName": "Senior Engineer",
            "postingUrl": "https://full.com/jobs/123",
            "status": "INTERVIEWED",
            "workModel": "HYBRID",
            "workLocation": "Warsaw",
            "compensations": [
                {
                    "minSalary": 10000,
                    "maxSalary": 15000,
                    "currency": "PLN",
                    "employmentType": "B2B",
                }
            ],
            "notes": "Interesting position",
        },
    )
    assert response.status_code == 201
    assert response.json()["id"]


@pytest.mark.integration
async def test_fails_with_empty_company_name(client):
    response = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "",
            "roleName": "Developer",
            "postingUrl": "https://test.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
        },
    )
    assert response.status_code == 422


@pytest.mark.integration
async def test_fails_with_empty_role_name(client):
    response = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Test Corp",
            "roleName": "",
            "postingUrl": "https://test.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
        },
    )
    assert response.status_code == 422


@pytest.mark.integration
async def test_fails_with_invalid_status(client):
    response = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Test Corp",
            "roleName": "Developer",
            "postingUrl": "https://test.com",
            "status": "INVALID_STATUS",
            "workModel": "REMOTE",
        },
    )
    assert response.status_code == 422


@pytest.mark.integration
async def test_fails_with_invalid_work_model(client):
    response = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Test Corp",
            "roleName": "Developer",
            "postingUrl": "https://test.com",
            "status": "APPLIED",
            "workModel": "INVALID_MODEL",
        },
    )
    assert response.status_code == 422


@pytest.mark.integration
async def test_fails_hybrid_without_location(client):
    response = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Test Corp",
            "roleName": "Developer",
            "postingUrl": "https://test.com",
            "status": "APPLIED",
            "workModel": "HYBRID",
            "workLocation": None,
        },
    )
    assert response.status_code == 400


@pytest.mark.integration
async def test_fails_onsite_without_location(client):
    response = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Test Corp",
            "roleName": "Developer",
            "postingUrl": "https://test.com",
            "status": "APPLIED",
            "workModel": "ONSITE",
        },
    )
    assert response.status_code == 400


@pytest.mark.integration
async def test_succeeds_remote_with_location(client):
    response = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Test Corp",
            "roleName": "Developer",
            "postingUrl": "https://test.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
            "workLocation": "Anywhere",
        },
    )
    assert response.status_code == 201


@pytest.mark.integration
async def test_fails_compensation_missing_currency(client):
    response = await client.post(
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
                    "currency": None,
                    "employmentType": "B2B",
                }
            ],
        },
    )
    assert response.status_code == 400


@pytest.mark.integration
async def test_fails_negative_min_salary(client):
    response = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Test Corp",
            "roleName": "Developer",
            "postingUrl": "https://test.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
            "compensations": [
                {
                    "minSalary": -1000,
                    "maxSalary": 8000,
                    "currency": "USD",
                    "employmentType": "B2B",
                }
            ],
        },
    )
    assert response.status_code == 400


@pytest.mark.integration
async def test_fails_min_salary_greater_than_max(client):
    response = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Test Corp",
            "roleName": "Developer",
            "postingUrl": "https://test.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
            "compensations": [
                {
                    "minSalary": 10000,
                    "maxSalary": 5000,
                    "currency": "USD",
                    "employmentType": "B2B",
                }
            ],
        },
    )
    assert response.status_code == 400


@pytest.mark.integration
async def test_fails_duplicate_employment_type(client):
    response = await client.post(
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
                    "maxSalary": 7000,
                    "currency": "USD",
                    "employmentType": "B2B",
                },
                {
                    "minSalary": 6000,
                    "maxSalary": 8000,
                    "currency": "USD",
                    "employmentType": "B2B",
                },
            ],
        },
    )
    assert response.status_code == 400


@pytest.mark.integration
async def test_fails_invalid_employment_type(client):
    response = await client.post(
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
                    "maxSalary": 7000,
                    "currency": "USD",
                    "employmentType": "INVALID",
                }
            ],
        },
    )
    assert response.status_code == 422


@pytest.mark.integration
async def test_succeeds_with_empty_compensations(client):
    response = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Test Corp",
            "roleName": "Developer",
            "postingUrl": "https://test.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
            "compensations": [],
        },
    )
    assert response.status_code == 201


@pytest.mark.integration
async def test_succeeds_with_multiple_compensations(client):
    response = await client.post(
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
                    "maxSalary": 7000,
                    "currency": "USD",
                    "employmentType": "B2B",
                },
                {
                    "minSalary": 4000,
                    "maxSalary": 6000,
                    "currency": "USD",
                    "employmentType": "PERMANENT",
                },
                {
                    "minSalary": 3000,
                    "maxSalary": 5000,
                    "currency": "USD",
                    "employmentType": "CONTRACT",
                },
            ],
        },
    )
    assert response.status_code == 201


@pytest.mark.integration
async def test_fails_missing_required_field(client):
    response = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Test Corp",
            "postingUrl": "https://test.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
        },
    )
    assert response.status_code == 422


@pytest.mark.integration
async def test_fails_null_required_field(client):
    response = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": None,
            "roleName": "Developer",
            "postingUrl": "https://test.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
        },
    )
    assert response.status_code == 422


@pytest.mark.integration
async def test_succeeds_with_null_notes(client):
    response = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": "Test Corp",
            "roleName": "Developer",
            "postingUrl": "https://test.com",
            "status": "APPLIED",
            "workModel": "REMOTE",
            "notes": None,
        },
    )
    assert response.status_code == 201


@pytest.mark.integration
@pytest.mark.parametrize(
    "status_value", ["APPLIED", "INTERVIEWED", "OFFERED", "ACCEPTED", "REJECTED"]
)
async def test_succeeds_with_status_values(client, status_value):
    response = await client.post(
        "/v1/job-applications/",
        json={
            "companyName": f"Corp {status_value}",
            "roleName": "Developer",
            "postingUrl": f"https://{status_value.lower()}.com",
            "status": status_value,
            "workModel": "REMOTE",
        },
    )
    assert response.status_code == 201
