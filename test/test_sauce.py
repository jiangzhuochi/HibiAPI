from pathlib import Path

import pytest
from fastapi.testclient import TestClient

REMOTE_SAUCE_URL = "https://i.loli.net/2021/02/08/ZF8GnifzDUAE1lc.jpg"
LOCAL_SAUCE_PATH = Path(__file__).parent / "test_sauce.jpg"


@pytest.fixture(scope="package")
def client():
    from hibiapi.app import app

    with TestClient(app, base_url="http://testserver/api/") as client:
        yield client


def test_sauce_url(client: TestClient):
    response = client.get("sauce/", params={"url": REMOTE_SAUCE_URL})
    assert response.status_code == 200
    if (data := response.json())["header"]["status"] == -2:
        pytest.skip(data["header"]["message"])
    assert data["header"]["status"] == 0, response.json()


def test_sauce_file(client: TestClient):
    with open(LOCAL_SAUCE_PATH, "rb") as file:
        response = client.post("sauce/", files={"file": file})
    assert response.status_code == 200
    if (data := response.json())["header"]["status"] == -2:
        pytest.skip(data["header"]["message"])
    assert data["header"]["status"] == 0, response.json()
