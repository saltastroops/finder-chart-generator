from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from starlette import status


def test_hrs_viewmodel_with_missing_values(client: TestClient):
    missing_values = [
        ("proposal_code", "proposal code"),
        ("principal_investigator", "Principal Investigator"),
        ("target", "target"),
        ("right_ascension", "right ascension"),
        ("declination", "declination"),
        ("position_angle", "position angle"),
    ]

    response = client.post("/hrs", data=dict())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    for field, missing_info in missing_values:
        assert missing_info in errors[field]


def test_hrs(client: TestClient) -> None:
    data = {
        "proposal_code": "2023-1-SCI-042",
        "principal_investigator": "Adams",
        "target": "Magrathea",
        "right_ascension": "42",
        "declination": "-42",
        "position_angle": "0",
        "image_survey": "POSS2/UKSTU Red",
    }
    response = client.post("/hrs", data=data)
    assert response.status_code == status.HTTP_200_OK


def test_imaging_viewmodel_with_missing_values(client: TestClient):
    missing_values = [
        ("proposal_code", "proposal code"),
        ("principal_investigator", "Principal Investigator"),
        ("target", "target"),
        ("right_ascension", "right ascension"),
        ("declination", "declination"),
        ("position_angle", "position angle"),
    ]

    response = client.post("/imaging", data=dict())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    for field, missing_info in missing_values:
        assert missing_info in errors[field]


def test_imaging(client: TestClient) -> None:
    data = {
        "proposal_code": "2023-1-SCI-042",
        "principal_investigator": "Adams",
        "target": "Magrathea",
        "right_ascension": "42",
        "declination": "-42",
        "position_angle": "0",
        "image_survey": "POSS2/UKSTU Red",
    }
    response = client.post("/imaging", data=data)
    assert response.status_code == status.HTTP_200_OK


def test_longslit_viewmodel_with_missing_values(client: TestClient):
    missing_values = [
        ("proposal_code", "proposal code"),
        ("principal_investigator", "Principal Investigator"),
        ("target", "target"),
        ("right_ascension", "right ascension"),
        ("declination", "declination"),
        ("slit_width", "slit width"),
        ("position_angle", "position angle"),
    ]

    response = client.post("/longslit", data=dict())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    for field, missing_info in missing_values:
        assert missing_info in errors[field]


def test_longslit(client: TestClient) -> None:
    data = {
        "proposal_code": "2023-1-SCI-042",
        "principal_investigator": "Adams",
        "target": "Magrathea",
        "right_ascension": "42",
        "declination": "-42",
        "slit_width": "3",
        "position_angle": "0",
        "image_survey": "POSS2/UKSTU Red",
    }
    response = client.post("/longslit", data=data)
    assert response.status_code == status.HTTP_200_OK


def test_mos_viewmodel_with_missing_values(client: TestClient):
    missing_values = [
        ("proposal_code", "proposal code"),
        ("principal_investigator", "Principal Investigator"),
        ("target", "target"),
        ("mos_mask_file", "MOS mask file"),
    ]

    response = client.post("/mos", data=dict())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    for field, missing_info in missing_values:
        assert missing_info in errors[field]


def test_mos(client: TestClient) -> None:
    data = {
        "proposal_code": "2023-1-SCI-042",
        "principal_investigator": "Adams",
        "target": "Magrathea",
        "position_angle": "0",
        "image_survey": "POSS2/UKSTU Red",
    }
    files = {"mos_mask_file": BytesIO(b"FITS")}
    response = client.post("/mos", data=data, files=files)
    assert response.status_code == status.HTTP_200_OK


def test_nir_viewmodel_with_missing_values(client: TestClient):
    missing_values = [
        ("proposal_code", "proposal code"),
        ("principal_investigator", "Principal Investigator"),
        ("target", "target"),
        ("right_ascension", "right ascension"),
        ("declination", "declination"),
        ("science_bundle_right_ascension", "right ascension of the science bundle"),
        ("science_bundle_declination", "declination of the science bundle"),
        ("nir_bundle_separation", "bundle separation"),
        ("position_angle", "position angle"),
    ]

    response = client.post("/nir", data=dict())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    for field, missing_info in missing_values:
        assert missing_info in errors[field]


def test_nir(client: TestClient) -> None:
    data = {
        "proposal_code": "2023-1-SCI-042",
        "principal_investigator": "Adams",
        "target": "Magrathea",
        "right_ascension": "42",
        "declination": "-42",
        "science_bundle_right_ascension": "42",
        "science_bundle_declination": "-42",
        "nir_bundle_separation": "123",
        "position_angle": "0",
        "image_survey": "POSS2/UKSTU Red",
    }
    response = client.post("/nir", data=data)
    assert response.status_code == status.HTTP_200_OK


def test_slotmode_viewmodel_with_missing_values(client: TestClient):
    missing_values = [
        ("proposal_code", "proposal code"),
        ("principal_investigator", "Principal Investigator"),
        ("target", "target"),
        ("right_ascension", "right ascension"),
        ("declination", "declination"),
        ("position_angle", "position angle"),
    ]

    response = client.post("/slotmode", data=dict())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    for field, missing_info in missing_values:
        assert missing_info in errors[field]


def test_slotmode(client: TestClient) -> None:
    data = {
        "proposal_code": "2023-1-SCI-042",
        "principal_investigator": "Adams",
        "target": "Magrathea",
        "right_ascension": "42",
        "declination": "-42",
        "position_angle": "0",
        "image_survey": "POSS2/UKSTU Red",
    }
    response = client.post("/slotmode", data=data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("url", ["/hrs", "/imaging", "/longslit", "/slotmode", "/nir"])
@pytest.mark.parametrize("value", ["invalid", "-0.1", "360.1"])
def test_invalid_right_ascension(url: str, value: str, client: TestClient) -> None:
    response = client.post(url, data={"right_ascension": value})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "360" in errors["right_ascension"]


@pytest.mark.parametrize("url", ["/hrs", "/imaging", "/longslit", "/slotmode", "/nir"])
@pytest.mark.parametrize("value", ["invalid", "-90.1", "90.1"])
def test_invalid_declination(url: str, value: str, client: TestClient) -> None:
    response = client.post(url, data={"declination": value})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "90" in errors["declination"]


@pytest.mark.parametrize("url", ["/hrs", "/imaging", "/longslit", "/slotmode", "/nir"])
@pytest.mark.parametrize("value", ["invalid", "-180.1", "180.1"])
def test_invalid_position_angle(url: str, value: str, client: TestClient) -> None:
    response = client.post(url, data={"position_angle": value})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "180" in errors["position_angle"]


@pytest.mark.parametrize("value", ["invalid", "0.49", "5.1"])
def test_invalid_slit_width(value: str, client: TestClient) -> None:
    response = client.post("/longslit", data={"slit_width": value})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "0.5" in errors["slit_width"]


@pytest.mark.parametrize("value", ["invalid", "-0.1", "360.1"])
def test_invalid_science_bundle_right_ascension(value: str, client: TestClient) -> None:
    response = client.post("/nir", data={"science_bundle_right_ascension": value})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "360" in errors["science_bundle_right_ascension"]


@pytest.mark.parametrize("value", ["invalid", "-90.1", "90.1"])
def test_invalid_science_bundle_declination(value: str, client: TestClient) -> None:
    response = client.post("/nir", data={"science_bundle_declination": value})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "90" in errors["science_bundle_declination"]


@pytest.mark.parametrize("value", ["invalid", "53.9", "165.1"])
def test_invalid_nir_bundle_separation(value: str, client: TestClient) -> None:
    response = client.post("/nir", data={"nir_bundle_separation": value})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "165" in errors["nir_bundle_separation"]


@pytest.mark.parametrize("url", ["/hrs", "/imaging", "/longslit"])
def test_background_image_errors(url: str, client: TestClient) -> None:
    # neither an image survey nor a custom FITS file given
    response = client.post(url, data=dict())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert (
        "image survey" in errors["__general"] and "custom FITS" in errors["__general"]
    )

    # an empty image survey is given
    response = client.post(url, data={"image_survey": ""})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "image_survey" in errors and "custom_fits" not in errors

    # an empty custom FITS file is given
    response = client.post(url, files={"custom_fits": BytesIO(b"")})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "image_survey" not in errors and "custom_fits" in errors

    # both an image survey and a custom FITS file are given
    response = client.post(
        url, data={"image_survey": ""}, files={"custom_fits": BytesIO(b"FITS")}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "mutually exclusive" in errors["__general"]
