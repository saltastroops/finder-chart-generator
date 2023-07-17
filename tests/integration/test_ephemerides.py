from datetime import datetime, timezone
from unittest import mock

import astropy.units as u
import pytest
from astropy.coordinates import SkyCoord
from imephu.utils import Ephemeris, MagnitudeRange
from starlette import status
from starlette.testclient import TestClient

import fcg.views.ephemerides

_URL = "/ephemerides"


def _valid_input() -> dict[str, str]:
    data = {
        "identifier": "567",
        "end": "1689681600",
        "output_interval": "30",
        "start": "1689595200",
    }
    return data


_mock_ephemerides = [
    Ephemeris(
        epoch=datetime(2023, 7, 17, 12, 0, 0, 0, tzinfo=timezone.utc),
        position=SkyCoord(ra=98.5 * u.deg, dec=-17.99 * u.deg),
        magnitude_range=MagnitudeRange(
            bandpass="V", min_magnitude=16.4, max_magnitude=16.4
        ),
    ),
    Ephemeris(
        epoch=datetime(2023, 7, 18, 12, 0, 0, 0, tzinfo=timezone.utc),
        position=SkyCoord(ra=98.43 * u.deg, dec=-18.34 * u.deg),
        magnitude_range=None,
    ),
]


def test_ephemerides_with_missing_values(client: TestClient) -> None:
    missing_values = [
        ("identifier", "Horizons identifier"),
        ("end", "end time"),
        ("output_interval", "output interval"),
        ("start", "start time"),
    ]

    response = client.post(_URL, data=dict())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    for field, missing_info in missing_values:
        assert missing_info in errors[field]


@pytest.mark.parametrize("offset", [0, 1])
def test_ephemerides_with_incorrect_start_end_order(
    offset: int, client: TestClient
) -> None:
    data = _valid_input()
    data["end"] = str(int(data["start"]) - offset)

    response = client.post(_URL, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.json()["errors"]
    assert "must be earlier" in errors["__general"]


def test_ephemerides(client: TestClient) -> None:
    data = _valid_input()

    with mock.patch.object(
        fcg.views.ephemerides, "HorizonsService"
    ) as MockHorizonsService:
        MockHorizonsService.return_value.ephemerides.return_value = _mock_ephemerides

        response = client.post(_URL, data=data)
        ephemerides = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(ephemerides) == 2

        assert (
            ephemerides[0]["epoch"]
            == datetime(2023, 7, 17, 12, 0, 0, 0, tzinfo=timezone.utc).timestamp()
        )
        assert ephemerides[0]["right_ascension"] == pytest.approx(98.5)
        assert ephemerides[1]["declination"] == pytest.approx(-18.34)
        assert ephemerides[0]["magnitude"] == 16.4
        assert ephemerides[1]["magnitude"] is None
