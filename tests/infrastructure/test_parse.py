from datetime import datetime, timezone
from typing import cast

import pytest
from starlette.datastructures import FormData

from fcg.infrastructure.parse import (
    is_float,
    parse_declination,
    parse_float,
    parse_generic_form_field,
    parse_int,
    parse_nir_bundle_separation,
    parse_position_angle,
    parse_right_ascension,
    parse_slit_width,
    parse_timestamp,
)


def test_parse_form_field_returns_value_from_parse_func() -> None:
    parsed_value = parse_generic_form_field(
        form=cast(FormData, {"a": "3"}),  # noqa
        field="a",
        parse_func=lambda s: 2 * int(s),
        default=0,
        missing_message="The value is missing.",
        error_id="a",
        errors=dict(),
    )
    assert parsed_value == 6


@pytest.mark.parametrize("form", [dict(), {"a": ""}, {"a": "\n \t"}])
def test_parse_form_field_handles_missing_value(form: dict[str, str]) -> None:
    missing_message = "The value is missing."
    errors: dict[str, str] = dict()
    parsed_value = parse_generic_form_field(
        form=cast(FormData, form),
        field="a",
        parse_func=lambda s: 2 * int(s),
        default=-42,
        missing_message=missing_message,
        error_id="a",
        errors=errors,
    )
    assert errors == {"a": missing_message}
    assert parsed_value == -42


def test_parse_form_field_returns_invalid_value() -> None:
    def f(s: str) -> str:
        raise ValueError(invalid_message)

    form = {"a": "not valid"}
    missing_message = "The value is missing."
    invalid_message = "The value is invalid."
    errors: dict[str, str] = dict()
    parsed_value = parse_generic_form_field(
        form=cast(FormData, form),
        field="a",
        parse_func=f,
        default="invalid",
        missing_message=missing_message,
        error_id="a",
        errors=errors,
    )
    assert errors == {"a": invalid_message}
    assert parsed_value == "invalid"


@pytest.mark.parametrize("text, expected", [("2", 2), ("0", 0), ("-17", -17)])
def test_parse_int(text: str, expected: int) -> None:
    int_value = parse_int(text)
    assert int_value == expected


@pytest.mark.parametrize("text", ["", "invalid"])
def test_parse_invalid_int(text: str) -> None:
    with pytest.raises(ValueError, match="int"):
        parse_int(text)


@pytest.mark.parametrize("text, expected", [("2.56", 2.56), ("0", 0), ("-17.8", -17.8)])
def test_parse_float(text: str, expected: float) -> None:
    float_value = parse_float(text)
    assert float_value == pytest.approx(expected)


@pytest.mark.parametrize("text", ["", "invalid"])
def test_parse_invalid_float(text: str) -> None:
    with pytest.raises(ValueError, match="float"):
        parse_float(text)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("0", datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)),
        ("1689591685", datetime(2023, 7, 17, 11, 1, 25, tzinfo=timezone.utc)),
    ],
)
def test_parse_timestamp(text: str, expected: datetime) -> None:
    assert parse_timestamp(text) == expected


@pytest.mark.parametrize("text", ["", "invalid"])
def test_parse_invalid_timestamp(text: str) -> None:
    with pytest.raises(ValueError, match="timestamp"):
        parse_timestamp(text)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("1h 30m", 22.5),
        ("225.16d", 225.16),
        ("123", 123),
        ("213.9", 213.9),
        ("0d", 0),
        ("360d", 360),
    ],
)
def test_parse_right_ascension(text: str, expected: float) -> None:
    right_ascension = parse_right_ascension(text)
    assert right_ascension.degree == pytest.approx(expected)


@pytest.mark.parametrize("text", ["", "invalid", "-0.01d", "360.01d"])
def test_parse_invalid_right_ascension(text: str) -> None:
    with pytest.raises(ValueError, match="360"):
        parse_right_ascension(text)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("-45d 30m", -45.5),
        ("2h", 30),
        ("-56", -56),
        ("16.9", 16.9),
        ("-90d", -90),
        ("90d", 90),
    ],
)
def test_parse_declination(text: str, expected: float) -> None:
    declination = parse_declination(text)
    assert declination.degree == pytest.approx(expected)


@pytest.mark.parametrize("text", ["", "invalid", "-90.01d", "90.01d"])
def test_parse_invalid_declination(text: str) -> None:
    with pytest.raises(ValueError, match="-90"):
        parse_declination(text)


@pytest.mark.parametrize(
    "text, expected", [("0.8", 0.8), ("3.984 arcsec", 3.984), ("0.5", 0.5), ("5", 5)]
)
def test_parse_slit_width(text: str, expected: float) -> None:
    slit_width = parse_slit_width(text)
    assert slit_width.arcsec == pytest.approx(expected)


@pytest.mark.parametrize("text", ["", "invalid", "0.499", "5.01"])
def test_parse_invalid_slit_width(text: str) -> None:
    with pytest.raises(ValueError, match="0.5"):
        parse_slit_width(text)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("-156d", -156),
        ("10h 30m", 157.5),
        ("-8.643", -8.643),
        ("+156", 156),
        ("-180d", -180),
        ("180d", 180),
    ],
)
def test_position_angle(text: str, expected: float) -> None:
    position_angle = parse_position_angle(text)
    assert position_angle.degree == pytest.approx(expected)


@pytest.mark.parametrize("text", ["", "invalid", "-180.001", "180.001"])
def test_invalid_position_angle(text: str) -> None:
    with pytest.raises(ValueError, match="-180"):
        parse_position_angle(text)


@pytest.mark.parametrize(
    "text, expected",
    [("89", 89), ("125.935 arcsec", 125.935), ("54", 54), ("165", 165)],
)
def test_nir_bundle_separation(text: str, expected: float) -> None:
    bundle_separation = parse_nir_bundle_separation(text)
    assert bundle_separation.arcsec == pytest.approx(float(expected))


@pytest.mark.parametrize("text", ["", "invalid", "53.999", "165.001"])
def test_parse_invalid_nir_bundle_separation(text: str) -> None:
    with pytest.raises(ValueError, match="165"):
        parse_nir_bundle_separation(text)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("-17.9", True),
        ("-5", True),
        ("+0.", True),
        ("+3", True),
        ("17.98", True),
        ("-", False),
        ("+", False),
        (".987", False),
        ("1e", False),
        ("five", False),
    ],
)
def test_is_float(text: str, expected: bool) -> None:
    assert is_float(text) is expected
