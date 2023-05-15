from starlette import status
from starlette.testclient import TestClient


def test_get_form(client: TestClient) -> None:
    # When I request the form
    response = client.get("/")

    # Then I get the form
    assert response.status_code == status.HTTP_200_OK
