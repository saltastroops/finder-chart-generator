from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from starlette import status


_URL = "/finder-charts"


@pytest.mark.parametrize("mode", ["", "invalid"])
def test_generate_for_invalid_mode(mode: str, client: TestClient) -> None:
    response = client.post(
        _URL, params={"mode": mode}, data={"imaging_survey": "POSS1 Red"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "mode" in errors["__general"]


@pytest.mark.parametrize("mode", ["MOS", "imaging", "LongSlit"])
def test_mode_is_case_insensitive(mode: str, client: TestClient) -> None:
    response = client.post(
        _URL, params={"mode": mode}, data={"image_survey": "POSS1 Red"}
    )
    errors = response.json()["errors"]
    assert "__general" not in errors


def test_generate_for_hrs_with_missing_values(client: TestClient):
    missing_values = [
        ("proposal_code", "proposal code"),
        ("principal_investigator", "Principal Investigator"),
        ("target", "target"),
        ("right_ascension", "right ascension"),
        ("declination", "declination"),
        ("position_angle", "position angle"),
    ]

    response = client.post(_URL, params={"mode": "hrs"}, data=dict())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    for field, missing_info in missing_values:
        assert missing_info in errors[field]


def test_generate_for_hrs(client: TestClient) -> None:
    data = {
        "proposal_code": "2023-1-SCI-042",
        "principal_investigator": "Adams",
        "target": "Magrathea",
        "right_ascension": "180",
        "declination": "-45",
        "position_angle": "0",
    }
    files = {"custom_fits": open("tests/data/ra12h_dec-45deg_10arcmin.fits", "rb")}
    response = client.post(_URL, params={"mode": "hrs"}, data=data, files=files)
    assert response.status_code == status.HTTP_200_OK


def test_generate_for_imaging_with_missing_values(client: TestClient):
    missing_values = [
        ("proposal_code", "proposal code"),
        ("principal_investigator", "Principal Investigator"),
        ("target", "target"),
        ("right_ascension", "right ascension"),
        ("declination", "declination"),
        ("position_angle", "position angle"),
    ]

    response = client.post(_URL, params={"mode": "imaging"}, data=dict())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    for field, missing_info in missing_values:
        assert missing_info in errors[field]


def test_generate_for_imaging(client: TestClient) -> None:
    data = {
        "proposal_code": "2023-1-SCI-042",
        "principal_investigator": "Adams",
        "target": "Magrathea",
        "right_ascension": "42",
        "declination": "-42",
        "position_angle": "0",
        "image_survey": "POSS2/UKSTU Red",
    }
    response = client.post(_URL, params={"mode": "imaging"}, data=data)
    assert response.status_code == status.HTTP_200_OK


def test_generate_for_longslit_with_missing_values(client: TestClient):
    missing_values = [
        ("proposal_code", "proposal code"),
        ("principal_investigator", "Principal Investigator"),
        ("target", "target"),
        ("right_ascension", "right ascension"),
        ("declination", "declination"),
        ("slit_width", "slit width"),
        ("position_angle", "position angle"),
    ]

    response = client.post(_URL, params={"mode": "longslit"}, data=dict())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    for field, missing_info in missing_values:
        assert missing_info in errors[field]


def test_generate_for_longslit(client: TestClient) -> None:
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
    response = client.post(_URL, params={"mode": "longslit"}, data=data)
    assert response.status_code == status.HTTP_200_OK


def test_generate_for_mos_with_missing_values(client: TestClient):
    missing_values = [
        ("proposal_code", "proposal code"),
        ("principal_investigator", "Principal Investigator"),
        ("target", "target"),
        ("mos_mask_file", "MOS mask file"),
    ]

    response = client.post(_URL, params={"mode": "mos"}, data=dict())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    for field, missing_info in missing_values:
        assert missing_info in errors[field]


def test_generate_for_mos(client: TestClient) -> None:
    data = {
        "proposal_code": "2023-1-SCI-042",
        "principal_investigator": "Adams",
        "target": "Magrathea",
        "position_angle": "0",
        "image_survey": "POSS2/UKSTU Red",
    }
    files = {"mos_mask_file": BytesIO(b"FITS")}
    response = client.post(_URL, params={"mode": "mos"}, data=data, files=files)
    assert response.status_code == status.HTTP_200_OK


def test_generate_for_nir_with_missing_values(client: TestClient):
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

    response = client.post(_URL, params={"mode": "nir"}, data=dict())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    for field, missing_info in missing_values:
        assert missing_info in errors[field]


def test_generate_for_nir(client: TestClient) -> None:
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
    response = client.post(_URL, params={"mode": "nir"}, data=data)
    assert response.status_code == status.HTTP_200_OK


def test_generate_for_slotmode_with_missing_values(client: TestClient):
    missing_values = [
        ("proposal_code", "proposal code"),
        ("principal_investigator", "Principal Investigator"),
        ("target", "target"),
        ("right_ascension", "right ascension"),
        ("declination", "declination"),
        ("position_angle", "position angle"),
    ]

    response = client.post(_URL, params={"mode": "slotmode"}, data=dict())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    for field, missing_info in missing_values:
        assert missing_info in errors[field]


def test_generate_for_slotmode(client: TestClient) -> None:
    data = {
        "proposal_code": "2023-1-SCI-042",
        "principal_investigator": "Adams",
        "target": "Magrathea",
        "right_ascension": "42",
        "declination": "-42",
        "position_angle": "0",
        "image_survey": "POSS2/UKSTU Red",
    }
    response = client.post(_URL, params={"mode": "slotmode"}, data=data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("mode", ["hrs", "imaging", "longslit", "slotmode", "nir"])
@pytest.mark.parametrize("value", ["invalid", "-0.1", "360.1"])
def test_invalid_right_ascension(mode: str, value: str, client: TestClient) -> None:
    response = client.post(_URL, params={"mode": mode}, data={"right_ascension": value})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "360" in errors["right_ascension"]


@pytest.mark.parametrize("mode", ["hrs", "imaging", "longslit", "slotmode", "nir"])
@pytest.mark.parametrize("value", ["invalid", "-90.1", "90.1"])
def test_invalid_declination(mode: str, value: str, client: TestClient) -> None:
    response = client.post(_URL, params={"mode": mode}, data={"declination": value})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "90" in errors["declination"]


@pytest.mark.parametrize("mode", ["hrs", "imaging", "longslit", "slotmode", "nir"])
@pytest.mark.parametrize("value", ["invalid", "-180.1", "180.1"])
def test_invalid_position_angle(mode: str, value: str, client: TestClient) -> None:
    response = client.post(_URL, params={"mode": mode}, data={"position_angle": value})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "180" in errors["position_angle"]


@pytest.mark.parametrize("value", ["invalid", "0.49", "5.1"])
def test_invalid_slit_width(value: str, client: TestClient) -> None:
    response = client.post(
        _URL, params={"mode": "longslit"}, data={"slit_width": value}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "0.5" in errors["slit_width"]


@pytest.mark.parametrize("value", ["invalid", "-0.1", "360.1"])
def test_invalid_science_bundle_right_ascension(value: str, client: TestClient) -> None:
    response = client.post(
        _URL, params={"mode": "nir"}, data={"science_bundle_right_ascension": value}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "360" in errors["science_bundle_right_ascension"]


@pytest.mark.parametrize("value", ["invalid", "-90.1", "90.1"])
def test_invalid_science_bundle_declination(value: str, client: TestClient) -> None:
    response = client.post(
        _URL, params={"mode": "nir"}, data={"science_bundle_declination": value}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "90" in errors["science_bundle_declination"]


@pytest.mark.parametrize("value", ["invalid", "53.9", "165.1"])
def test_invalid_nir_bundle_separation(value: str, client: TestClient) -> None:
    response = client.post(
        _URL, params={"mode": "nir"}, data={"nir_bundle_separation": value}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "165" in errors["nir_bundle_separation"]


@pytest.mark.parametrize(
    "mode", ["hrs", "imaging", "longslit", "mos", "nir", "slotmode"]
)
def test_background_image_errors(mode: str, client: TestClient) -> None:
    # neither an image survey nor a custom FITS file given
    response = client.post(_URL, params={"mode": mode}, data=dict())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert (
        "image survey" in errors["__general"] and "custom FITS" in errors["__general"]
    )

    # an empty image survey is given
    response = client.post(_URL, params={"mode": mode}, data={"image_survey": ""})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "image_survey" in errors and "custom_fits" not in errors

    # an empty custom FITS file is given
    response = client.post(
        _URL, params={"mode": mode}, files={"custom_fits": BytesIO(b"")}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "image_survey" not in errors and "custom_fits" in errors

    # both an image survey and a custom FITS file are given
    response = client.post(
        _URL,
        params={"mode": mode},
        data={"image_survey": ""},
        files={"custom_fits": BytesIO(b"FITS")},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "mutually exclusive" in errors["__general"]

    # the image survey does not cover the position on the sky
    response = client.post(
        _URL,
        params={"mode": mode},
        data={
            "image_survey": "POSS1 Red",
            "right_ascension": "1",
            "declination": "-50",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "cover" in errors["image_survey"]
