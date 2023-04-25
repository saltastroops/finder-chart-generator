from typing import cast

from astropy.coordinates import Angle
from starlette.datastructures import FormData, UploadFile

from infrastructure import parse


def parse_proposal_code(form: FormData, errors: dict[str, str]) -> str | None:
    return parse.parse_generic_form_field(
        form=form,
        field="proposal_code",
        parse_func=lambda s: s,
        missing_message="The proposal code is missing.",
        error_id="proposal_code",
        errors=errors,
    )


def parse_principal_investigator(form: FormData, errors: dict[str, str]) -> str | None:
    return parse.parse_generic_form_field(
        form=form,
        field="principal_investigator",
        parse_func=lambda s: s,
        missing_message="The Principal Investigator is missing.",
        error_id="principal_investigator",
        errors=errors,
    )


def parse_target(form: FormData, errors: dict[str, str]) -> str | None:
    return parse.parse_generic_form_field(
        form=form,
        field="target",
        parse_func=lambda s: s,
        missing_message="The target is missing.",
        error_id="target",
        errors=errors,
    )


def parse_right_ascension(form: FormData, errors: dict[str, str]) -> Angle | None:
    return parse.parse_generic_form_field(
        form=form,
        field="right_ascension",
        parse_func=parse.parse_right_ascension,
        missing_message="The right ascension is missing.",
        error_id="right_ascension",
        errors=errors,
    )


def parse_declination(form: FormData, errors: dict[str, str]) -> Angle | None:
    return parse.parse_generic_form_field(
        form=form,
        field="declination",
        parse_func=parse.parse_declination,
        missing_message="The declination is missing.",
        error_id="declination",
        errors=errors,
    )


def parse_slit_width(form: FormData, errors: dict[str, str]) -> Angle | None:
    return parse.parse_generic_form_field(
        form=form,
        field="slit_width",
        parse_func=parse.parse_slit_width,
        missing_message="The slit width is missing.",
        error_id="slit_width",
        errors=errors,
    )


def parse_position_angle(form: FormData, errors: dict[str, str]) -> Angle | None:
    return parse.parse_generic_form_field(
        form=form,
        field="position_angle",
        parse_func=parse.parse_position_angle,
        missing_message="The position angle is missing.",
        error_id="position_angle",
        errors=errors,
    )


def parse_background_image(
    form: FormData, errors: dict[str, str]
) -> str | UploadFile | None:
    if "image_survey" in form:
        if form.get("image_survey"):
            return form.get("image_survey")
        else:
            errors["image_survey"] = "The image survey is missing."
            return None
    elif "custom_fits" in form:
        if form.get("custom_fits").size > 0:
            return cast(UploadFile, form.get("custom_fits"))
        else:
            errors["custom_fits"] = "The custom FITS file is missing."
            return None
    else:
        errors["__general"] = "An image survey or a custom FITS file must be supplied."
        return None
