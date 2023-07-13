from io import BufferedReader, BytesIO
from typing import Callable, Tuple

import numpy as np
import pytest
from fastapi.testclient import TestClient
from starlette import status

_CheckImage = Callable[[bytes], None]


_URL = "/finder-charts"


def _valid_input(mode: str) -> Tuple[dict[str, str], dict[str, BufferedReader]]:
    data = {
        "proposal_code": "2023-1-SCI-042",
        "principal_investigator": "Adams",
        "target": "Magrathea",
        "right_ascension": "170.1",
        "declination": "-55.5",
        "position_angle": "30",
        "output_format": "png",
    }
    files = {"custom_fits": open("tests/data/ra170.1_dec-55.5.fits", "rb")}
    match mode:
        case "hrs":
            pass
        case "imaging":
            pass
        case "longslit":
            data["slit_width"] = "4"
        case "mos":
            del data["right_ascension"]
            del data["declination"]
            files["mos_mask_file"] = open("tests/data/mos_mask.xml", "rb")
        case "nir":
            data["science_bundle_right_ascension"] = "180d 1m"
            data["science_bundle_declination"] = "-45d 2m"
            data["nir_bundle_separation"] = "100"
        case "slotmode":
            pass
        case _:
            raise ValueError(f"Unsupported mode: {mode}")

    return data, files


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


def test_generate_for_hrs_with_missing_values(client: TestClient) -> None:
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


def test_generate_for_hrs(client: TestClient, check_image: _CheckImage) -> None:
    np.random.seed(0)
    data, files = _valid_input("hrs")
    response = client.post(_URL, params={"mode": "hrs"}, data=data, files=files)
    assert response.status_code == status.HTTP_200_OK
    check_image(response.content)


def test_generate_for_imaging_with_missing_values(client: TestClient) -> None:
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


def test_generate_for_imaging(client: TestClient, check_image: _CheckImage) -> None:
    data, files = _valid_input("imaging")
    response = client.post(_URL, params={"mode": "imaging"}, data=data, files=files)
    assert response.status_code == status.HTTP_200_OK
    check_image(response.content)


def test_generate_for_longslit_with_missing_values(client: TestClient) -> None:
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


def test_generate_for_longslit(client: TestClient, check_image: _CheckImage) -> None:
    data, files = _valid_input("longslit")
    response = client.post(_URL, params={"mode": "longslit"}, data=data, files=files)
    assert response.status_code == status.HTTP_200_OK
    check_image(response.content)


def test_generate_for_mos_with_missing_values(client: TestClient) -> None:
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


def test_generate_for_mos(client: TestClient, check_image: _CheckImage) -> None:
    data, files = _valid_input("mos")
    response = client.post(_URL, params={"mode": "mos"}, data=data, files=files)
    assert response.status_code == status.HTTP_200_OK
    check_image(response.content)


def test_generate_for_nir_with_missing_values(client: TestClient) -> None:
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


def test_generate_for_nir(client: TestClient, check_image: _CheckImage) -> None:
    data, files = _valid_input("nir")
    response = client.post(_URL, params={"mode": "nir"}, data=data, files=files)
    assert response.status_code == status.HTTP_200_OK
    check_image(response.content)


def test_generate_for_slotmode_with_missing_values(client: TestClient) -> None:
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


def test_generate_for_slotmode(client: TestClient, check_image: _CheckImage) -> None:
    data, files = _valid_input("slotmode")
    response = client.post(_URL, params={"mode": "slotmode"}, data=data, files=files)
    assert response.status_code == status.HTTP_200_OK
    check_image(response.content)


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


@pytest.mark.parametrize(
    "mode", ["hrs", "imaging", "longslit", "mos", "nir", "slotmode"]
)
def test_generate_for_invalid_output_format(mode: str, client: TestClient) -> None:
    data, files = _valid_input(mode)
    data["output_format"] = "invalid"
    response = client.post(_URL, params={"mode": "hrs"}, data=data, files=files)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "unsupported" in errors["output_format"].lower()
