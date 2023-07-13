from typing import cast

import pytest
from starlette.datastructures import FormData

from fcg.viewmodels.parse import parse_magnitude_range


@pytest.mark.parametrize(
    "min_magnitude_text, max_magnitude_text, bandpass_text, error",
    [
        ("16", "17", None, "bandpass"),
        ("16", None, "V", "bandpass"),
        (None, "17", "V", "bandpass"),
        ("17", "16.99", "V", "greater"),
    ],
)
def test_parse_invalid_magnitude_range(
    min_magnitude_text: str | None,
    max_magnitude_text: str | None,
    bandpass_text: str | None,
    error: str,
) -> None:
    form = cast(
        FormData,
        {
            "min_magnitude": min_magnitude_text,
            "max_magnitude": max_magnitude_text,
            "bandpass": bandpass_text,
        },
    )
    errors = dict()
    magnitude_range = parse_magnitude_range(form, errors)
    assert magnitude_range is None
    assert error in errors["magnitude_range"]


@pytest.mark.parametrize(
    "min_magnitude, max_magnitude, bandpass",
    [(-4, -4, "V"), (-6.78, 1.8, "B"), (17.94, 17.94, "SRE-1")],
)
def test_parse_magnitude_range(min_magnitude, max_magnitude, bandpass) -> None:
    form = cast(
        FormData,
        {
            "min_magnitude": str(min_magnitude),
            "max_magnitude": str(max_magnitude),
            "bandpass": bandpass,
        },
    )
    errors = dict()
    magnitude_range = parse_magnitude_range(form, errors)
    assert pytest.approx(magnitude_range.min_magnitude) == min_magnitude
    assert pytest.approx(magnitude_range.max_magnitude) == max_magnitude
    assert magnitude_range.bandpass == bandpass
    assert len(errors) == 0
