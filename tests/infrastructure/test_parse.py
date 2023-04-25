from typing import cast

import pytest
from starlette.datastructures import FormData

from infrastructure.parse import (
    is_float,
    parse_declination,
    parse_generic_form_field,
    parse_nir_bundle_separation,
    parse_position_angle,
    parse_right_ascension,
    parse_slit_width,
)


def test_parse_form_field_returns_value_from_parse_func() -> None:
    parsed_value = parse_generic_form_field(
        form=cast(FormData, {"a": "3"}),  # noqa
        field="a",
        parse_func=lambda s: 2 * int(s),
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
        missing_message=missing_message,
        error_id="a",
        errors=errors,
    )
    assert errors == {"a": missing_message}
    assert parsed_value is None


def test_parse_form_field_returns_invalid_value() -> None:
    assert len("ppp") == 1


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
