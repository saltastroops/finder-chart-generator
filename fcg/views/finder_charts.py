import logging
import pathlib
import tempfile
from io import BytesIO
from typing import BinaryIO, Tuple, cast

from astropy import units as u
from astropy.coordinates import Angle, SkyCoord
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from imephu.finder_chart import FinderChart
from imephu.salt.finder_chart import (
    GeneralProperties,
    Target,
    hrs_finder_chart,
    nir_finder_chart,
    rss_longslit_finder_chart,
    rss_mos_finder_chart,
    salticam_finder_chart,
)
from imephu.salt.utils import MosMask
from imephu.service.survey import load_fits
from starlette import status
from starlette.datastructures import UploadFile
from starlette.responses import StreamingResponse

from fcg.viewmodels.base_viewmodel import OutputFormat
from fcg.viewmodels.hrs_viewmodel import HrsViewModel
from fcg.viewmodels.imaging_viewmodel import ImagingViewModel
from fcg.viewmodels.longslit_viewmodel import LongslitViewModel
from fcg.viewmodels.mos_viewmodel import MosViewModel
from fcg.viewmodels.nir_viewmodel import NirViewModel
from fcg.viewmodels.slotmode_viewmodel import SlotmodeViewModel

router = APIRouter()


@router.post("/finder-charts")
async def generate_finder_chart(request: Request, mode: str) -> Response:
    try:
        match mode.lower():
            case "hrs":
                return await _hrs(request)
            case "imaging":
                return await _imaging(request)
            case "longslit":
                return await _longslit(request)
            case "mos":
                return await _mos(request)
            case "nir":
                return await _nir(request)
            case "slotmode":
                return await _slotmode(request)
            case _:
                errors = {
                    "__general": f"Unsupported finder chart generation mode: {mode}"
                }
                return JSONResponse(
                    {"errors": errors}, status_code=status.HTTP_400_BAD_REQUEST
                )
    except Exception as e:
        logging.log(logging.ERROR, str(e))
        return JSONResponse(
            {"errors": {"__general": str(e)}},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def _hrs(request: Request) -> Response:
    vm = HrsViewModel(request)

    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    position = SkyCoord(ra=vm.right_ascension, dec=vm.declination)
    survey, fits = _fits_details(vm.background_image, position)
    general_properties = _general_properties(
        principal_investigator=vm.principal_investigator,
        proposal_code=vm.proposal_code,
        target=vm.target,
        position=position,
        position_angle=vm.position_angle,
        survey=survey,
    )
    finder_chart = hrs_finder_chart(fits=fits, general=general_properties)

    return _finder_chart_stream(finder_chart, vm.output_format)


async def _imaging(request: Request) -> Response:
    vm = ImagingViewModel(request)

    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    position = SkyCoord(ra=vm.right_ascension, dec=vm.declination)
    survey, fits = _fits_details(vm.background_image, position)
    general_properties = _general_properties(
        principal_investigator=vm.principal_investigator,
        proposal_code=vm.proposal_code,
        target=vm.target,
        position=position,
        position_angle=vm.position_angle,
        survey=survey,
    )
    finder_chart = salticam_finder_chart(
        fits=fits, general=general_properties, is_slot_mode=False
    )
    return _finder_chart_stream(finder_chart, vm.output_format)


async def _longslit(request: Request) -> Response:
    vm = LongslitViewModel(request)

    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    position = SkyCoord(ra=vm.right_ascension, dec=vm.declination)
    survey, fits = _fits_details(vm.background_image, position)
    general_properties = _general_properties(
        principal_investigator=vm.principal_investigator,
        proposal_code=vm.proposal_code,
        target=vm.target,
        position=position,
        position_angle=vm.position_angle,
        survey=survey,
    )
    finder_chart = rss_longslit_finder_chart(
        fits=fits,
        general=general_properties,
        slit_width=vm.slit_width,
        slit_height=8 * u.arcmin,
    )
    return _finder_chart_stream(finder_chart, vm.output_format)


async def _mos(request: Request) -> Response:
    vm = MosViewModel(request)

    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    mos_mask = await _mos_mask(cast(UploadFile, vm.mos_mask_file))
    position = mos_mask.center
    survey, fits = _fits_details(vm.background_image, position)
    general_properties = _general_properties(
        principal_investigator=vm.principal_investigator,
        proposal_code=vm.proposal_code,
        target=vm.target,
        position=position,
        position_angle=mos_mask.position_angle,
        survey=survey,
    )
    finder_chart = rss_mos_finder_chart(
        fits=fits, general=general_properties, mos_mask=mos_mask
    )
    return _finder_chart_stream(finder_chart, vm.output_format)


async def _nir(request: Request) -> Response:
    vm = NirViewModel(request)

    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    position = SkyCoord(ra=vm.right_ascension, dec=vm.declination)
    survey, fits = _fits_details(vm.background_image, position)
    general_properties = _general_properties(
        principal_investigator=vm.principal_investigator,
        proposal_code=vm.proposal_code,
        target=vm.target,
        position=position,
        position_angle=vm.position_angle,
        survey=survey,
    )
    science_bundle_center = SkyCoord(
        ra=vm.science_bundle_right_ascension, dec=vm.science_bundle_declination
    )
    finder_chart = nir_finder_chart(
        fits=fits,
        general=general_properties,
        science_bundle_center=science_bundle_center,
        bundle_separation=vm.nir_bundle_separation,
    )
    return _finder_chart_stream(finder_chart, vm.output_format)


async def _slotmode(request: Request) -> Response:
    vm = SlotmodeViewModel(request)

    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    position = SkyCoord(ra=vm.right_ascension, dec=vm.declination)
    survey, fits = _fits_details(vm.background_image, position)
    general_properties = _general_properties(
        principal_investigator=vm.principal_investigator,
        proposal_code=vm.proposal_code,
        target=vm.target,
        position=position,
        position_angle=vm.position_angle,
        survey=survey,
    )
    finder_chart = salticam_finder_chart(
        fits=fits, general=general_properties, is_slot_mode=True
    )
    return _finder_chart_stream(finder_chart, vm.output_format)


def _general_properties(
    principal_investigator: str,
    proposal_code: str,
    target: str,
    position: SkyCoord,
    position_angle: Angle,
    survey: str = "",
) -> GeneralProperties:
    return GeneralProperties(
        target=Target(
            name=target,
            position=position,
            magnitude_range=None,
        ),
        position_angle=position_angle,
        automated_position_angle=False,
        proposal_code=proposal_code,
        pi_family_name=principal_investigator,
        survey=survey,
    )


def _fits_details(
    background_image: str | UploadFile, position: SkyCoord
) -> Tuple[str, BinaryIO]:
    if type(background_image) == str:
        survey = background_image
        return survey, load_fits(
            survey=survey, fits_center=position, size=10 * u.arcmin
        )
    elif hasattr(background_image, "file"):
        survey = ""
        return survey, cast(UploadFile, background_image).file
    else:
        # Should never happen...
        raise ValueError("Either a survey or a FITS file is required")


async def _mos_mask(mos_mask_file: UploadFile) -> MosMask:
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(await mos_mask_file.read())
        fp.seek(0)
        return MosMask.from_file(pathlib.Path(fp.name))


def _finder_chart_stream(
    finder_chart: FinderChart, output_format: OutputFormat
) -> StreamingResponse:
    content = BytesIO()
    finder_chart.save(content, format=output_format)
    content.seek(0)

    match output_format:
        case "pdf":
            media_type = "application/pdf"
        case "png":
            media_type = "image/png"
        case _:
            # should never happen
            raise ValueError(f"Unsupported output format: {output_format}")

    return StreamingResponse(content, media_type=media_type)
