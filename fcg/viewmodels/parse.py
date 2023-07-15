from typing import cast

from astropy.coordinates import Angle, SkyCoord
from imephu.service.survey import is_covering_position
from starlette.datastructures import FormData, UploadFile

from fcg.infrastructure import parse
from fcg.infrastructure.types import MagnitudeRange, OutputFormat


def parse_proposal_code(form: FormData, errors: dict[str, str]) -> str:
    return parse.parse_generic_form_field(
        form=form,
        field="proposal_code",
        parse_func=lambda s: s,
        default="",
        missing_message="The proposal code is missing.",
        error_id="proposal_code",
        errors=errors,
    )


def parse_principal_investigator(form: FormData, errors: dict[str, str]) -> str:
    return parse.parse_generic_form_field(
        form=form,
        field="principal_investigator",
        parse_func=lambda s: s,
        default="",
        missing_message="The Principal Investigator is missing.",
        error_id="principal_investigator",
        errors=errors,
    )


def parse_target(form: FormData, errors: dict[str, str]) -> str:
    return parse.parse_generic_form_field(
        form=form,
        field="target",
        parse_func=lambda s: s,
        default="",
        missing_message="The target is missing.",
        error_id="target",
        errors=errors,
    )


def parse_magnitude_range(
    form: FormData, errors: dict[str, str]
) -> MagnitudeRange | None:
    min_magnitude_value = form.get("min_magnitude")
    max_magnitude_value = form.get("max_magnitude")
    bandpass_value = form.get("bandpass")
    non_none_count = (
        (1 if min_magnitude_value is not None else 0)
        + (1 if max_magnitude_value is not None else 0)
        + (1 if bandpass_value is not None else 0)
    )
    if non_none_count == 0:
        return None
    elif non_none_count == 3:
        min_magnitude = parse.parse_generic_form_field(
            form=form,
            field="min_magnitude",
            parse_func=parse.parse_float,
            default=0.0,
            missing_message="The minimum magnitude is missing.",
            error_id="magnitude_range",
            errors=errors,
        )
        max_magnitude = parse.parse_generic_form_field(
            form=form,
            field="max_magnitude",
            parse_func=parse.parse_float,
            default=0.0,
            missing_message="The maximum magnitude is missing.",
            error_id="magnitude_range",
            errors=errors,
        )
        bandpass = parse.parse_generic_form_field(
            form=form,
            field="bandpass",
            parse_func=lambda s: s,
            default="",
            missing_message="The bandpass is missing.",
            error_id="magnitude_range",
            errors=errors,
        )
        if min_magnitude is None or max_magnitude is None or bandpass is None:
            return None

        if max_magnitude < min_magnitude:
            errors["magnitude_range"] = (
                "The minimum magnitude must not be greater "
                "than the maximum magnitude."
            )
            return None

        return MagnitudeRange(
            min_magnitude=min_magnitude, max_magnitude=max_magnitude, bandpass=bandpass
        )
    else:
        errors[
            "magnitude_range"
        ] = "A minimum magnitude, maximum magnitude and bandpass must be specified for a magnitude range."
        return None


def parse_right_ascension(form: FormData, errors: dict[str, str]) -> Angle:
    return parse.parse_generic_form_field(
        form=form,
        field="right_ascension",
        parse_func=parse.parse_right_ascension,
        default=Angle("0deg"),
        missing_message="The right ascension is missing.",
        error_id="right_ascension",
        errors=errors,
    )


def parse_declination(form: FormData, errors: dict[str, str]) -> Angle:
    return parse.parse_generic_form_field(
        form=form,
        field="declination",
        parse_func=parse.parse_declination,
        default=Angle("0deg"),
        missing_message="The declination is missing.",
        error_id="declination",
        errors=errors,
    )


def parse_slit_width(form: FormData, errors: dict[str, str]) -> Angle:
    return parse.parse_generic_form_field(
        form=form,
        field="slit_width",
        parse_func=parse.parse_slit_width,
        default=Angle("0deg"),
        missing_message="The slit width is missing.",
        error_id="slit_width",
        errors=errors,
    )


def parse_position_angle(form: FormData, errors: dict[str, str]) -> Angle:
    return parse.parse_generic_form_field(
        form=form,
        field="position_angle",
        parse_func=parse.parse_position_angle,
        default=Angle("0deg"),
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


def parse_reference_star_right_ascension(
    form: FormData, errors: dict[str, str]
) -> Angle | None:
    if not form.get("reference_star_right_ascension") and not form.get(
        "reference_star_declination"
    ):
        return None
    return parse.parse_generic_form_field(
        form=form,
        field="reference_star_right_ascension",
        parse_func=parse.parse_right_ascension,
        default=Angle("0deg"),
        missing_message="The right ascension of the reference star is missing.",
        error_id="reference_star_right_ascension",
        errors=errors,
    )


def parse_reference_star_declination(form: FormData, errors: dict[str, str]) -> Angle:
    if not form.get("reference_star_right_ascension") and not form.get(
        "reference_star_declination"
    ):
        return Angle("0deg")
    return parse.parse_generic_form_field(
        form=form,
        field="reference_star_declination",
        parse_func=parse.parse_declination,
        default=Angle("0deg"),
        missing_message="The declination of the reference star is missing.",
        error_id="reference_star_declination",
        errors=errors,
    )


def parse_nir_bundle_separation(form: FormData, errors: dict[str, str]) -> Angle:
    return parse.parse_generic_form_field(
        form=form,
        field="nir_bundle_separation",
        parse_func=parse.parse_nir_bundle_separation,
        default=Angle("0deg"),
        missing_message="The bundle separation is missing.",
        error_id="nir_bundle_separation",
        errors=errors,
    )


def parse_background_image(form: FormData, errors: dict[str, str]) -> str | UploadFile:
    if "image_survey" in form and "custom_fits" in form:
        errors[
            "__general"
        ] = "The image survey and custom FITS file are mutually exclusive."
        return ""
    elif "image_survey" in form:
        if form.get("image_survey"):
            survey = cast(str, form.get("image_survey"))
            if _is_position_covered_by_survey(form, survey):
                return survey
            else:
                errors["image_survey"] = (
                    "The image survey does not cover the selected right ascension "
                    "and declination."
                )
                return ""
        else:
            errors["image_survey"] = "The image survey is missing."
            return ""
    elif "custom_fits" in form:
        if cast(int, cast(UploadFile, form.get("custom_fits")).size) > 0:
            return cast(UploadFile, form.get("custom_fits"))
        else:
            errors["custom_fits"] = "The custom FITS file is missing."
            return ""
    else:
        errors["__general"] = "An image survey or a custom FITS file must be supplied."
        return ""


def parse_output_format(form: FormData, errors: dict[str, str]) -> OutputFormat:
    output_format = cast(str, form.get("output_format", "pdf")).strip()
    match output_format.lower():
        case "pdf":
            return "pdf"
        case "png":
            return "png"
        case _:
            errors["output_format"] = f"Unsupported output format: {output_format}"
            return "pdf"


def _is_position_covered_by_survey(form: FormData, survey: str) -> bool:
    try:
        right_ascension = parse.parse_right_ascension(
            cast(str, form.get("right_ascension", ""))
        )
        declination = parse.parse_declination(cast(str, form.get("declination", "")))
    except ValueError:
        return True
    return is_covering_position(survey, SkyCoord(ra=right_ascension, dec=declination))
