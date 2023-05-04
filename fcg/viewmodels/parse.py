from typing import cast

from astropy.coordinates import Angle, SkyCoord
from imephu.service.survey import is_covering_position
from starlette.datastructures import FormData, UploadFile

from fcg.viewmodels.base_viewmodel import OutputFormat
from fcg.infrastructure import parse


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


def parse_mos_mask_file(form: FormData, errors: dict[str, str]) -> UploadFile | None:
    missing_error = "The MOS mask file is missing."
    if "mos_mask_file" not in form:
        errors["mos_mask_file"] = missing_error
        return None
    mos_mask_file = cast(UploadFile, form["mos_mask_file"])
    if mos_mask_file.size == 0:
        errors["mos_mask_file"] = missing_error
        return None
    return mos_mask_file


def parse_science_bundle_right_ascension(
    form: FormData, errors: dict[str, str]
) -> Angle | None:
    return parse.parse_generic_form_field(
        form=form,
        field="science_bundle_right_ascension",
        parse_func=parse.parse_right_ascension,
        missing_message="The right ascension of the science bundle is missing.",
        error_id="science_bundle_right_ascension",
        errors=errors,
    )


def parse_science_bundle_declination(
    form: FormData, errors: dict[str, str]
) -> Angle | None:
    return parse.parse_generic_form_field(
        form=form,
        field="science_bundle_declination",
        parse_func=parse.parse_declination,
        missing_message="The declination of the science bundle is missing.",
        error_id="science_bundle_declination",
        errors=errors,
    )


def parse_nir_bundle_separation(form: FormData, errors: dict[str, str]) -> Angle | None:
    return parse.parse_generic_form_field(
        form=form,
        field="nir_bundle_separation",
        parse_func=parse.parse_nir_bundle_separation,
        missing_message="The bundle separation is missing.",
        error_id="nir_bundle_separation",
        errors=errors,
    )


def parse_background_image(
    form: FormData, errors: dict[str, str]
) -> str | UploadFile | None:
    if "image_survey" in form and "custom_fits" in form:
        errors[
            "__general"
        ] = "The image survey and custom FITS file are mutually exclusive."
        return None
    elif "image_survey" in form:
        if form.get("image_survey"):
            survey = form.get("image_survey")
            if _is_position_covered_by_survey(form, survey):
                return survey
            else:
                errors["image_survey"] = (
                    "The image survey does not cover the selected right ascension "
                    "and declination."
                )
                return None
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


def parse_output_format(form: FormData, errors: dict[str, str]) -> OutputFormat | None:
    output_format = form.get("output_format", "pdf").strip()
    match output_format.lower():
        case "pdf":
            return "pdf"
        case "png":
            return "png"
        case _:
            errors["output_format"] = f"Unsupported output format: {output_format}"
            return None


def _is_position_covered_by_survey(form: FormData, survey: str) -> bool:
    try:
        right_ascension = parse.parse_right_ascension(form.get("right_ascension", ""))
        declination = parse.parse_declination(form.get("declination", ""))
    except ValueError:
        return True
    return is_covering_position(survey, SkyCoord(ra=right_ascension, dec=declination))
