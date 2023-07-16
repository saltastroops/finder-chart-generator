import re
from typing import Callable, TypeVar, cast

from astropy.coordinates import Angle
from starlette.datastructures import FormData

T = TypeVar("T")


def parse_generic_form_field(
    form: FormData,
    field: str,
    parse_func: Callable[[str], T],
    default: T,
    missing_message: str,
    error_id: str,
    errors: dict[str, str],
) -> T:
    field_value = cast(str, form.get(field, "")).strip()
    if not field_value:
        errors[error_id] = missing_message
        return default
    try:
        return parse_func(field_value)
    except ValueError as e:
        errors[error_id] = str(e)
        return default


def parse_float(text: str) -> float:
    """
    Parse a float value.
    """
    error = f"Not a float value: {text}"
    if not is_float(text):
        raise ValueError(error)
    return float(text)


def parse_right_ascension(text: str) -> Angle:
    """
    Parse a right ascension value.

    The value is returned as an AstroPy Angle instance.
    """
    error = "The right ascension must be an angle between 0 and 360 degrees."
    if is_float(text):
        text = text + "d"
    try:
        angle = Angle(text)
    except BaseException:
        raise ValueError(error) from None
    if angle.degree < 0 or angle.degree > 360:
        raise ValueError(error)
    return angle


def parse_declination(text: str) -> Angle:
    """
    Parse a declination value.

    The value is returned as an AstroPy Angle instance
    """
    error = "The declination must be an angle between -90 and 90 degrees."
    if is_float(text):
        text = text + "d"
    try:
        angle = Angle(text)
    except ValueError:
        raise ValueError(error) from None
    if angle.degree < -90 or angle.degree > 90:
        raise ValueError(error)
    return angle


def parse_slit_width(text: str) -> Angle:
    """
    Parse a slit width value.

    The value is returned as an AstroPy Angle instance
    """
    error = "The slit width must be an angle between 0.5 and 5 arcseconds."
    if is_float(text):
        text = text + "arcsec"
    try:
        angle = Angle(text)
    except ValueError:
        raise ValueError(error) from None
    if angle.arcsecond < 0.5 or angle.arcsecond > 5:
        raise ValueError(error)
    return angle


def parse_position_angle(text: str) -> Angle:
    """
    Parse a position angle value.

    The value is returned as an AstroPy Angle instance
    """
    error = "The slit width must be an angle between -180 and +180 degrees."
    if is_float(text):
        text = text + "d"
    try:
        angle = Angle(text)
    except ValueError:
        raise ValueError(error) from None
    if angle.degree < -180 or angle.degree > 180:
        raise ValueError(error)
    return angle


def parse_nir_bundle_separation(text: str) -> Angle:
    """
    Parse a slit width value.

    The value is returned as an AstroPy Angle instance
    """
    error = "The slit width must be an angle between 54 and 165 arcseconds."
    if is_float(text):
        text = text + "arcsec"
    try:
        angle = Angle(text)
    except ValueError:
        raise ValueError(error) from None
    if angle.arcsecond < 54 or angle.arcsecond > 165:
        raise ValueError(error)
    return angle


def is_float(text: str) -> bool:
    return re.match(r"^[+-]?\d+(?:\.\d*)?$", text) is not None
