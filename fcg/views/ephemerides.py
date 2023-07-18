import astropy.units as u
from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from imephu.service.horizons import HorizonsService
from starlette import status
from starlette.requests import Request

from fcg.viewmodels.ephemerides_viewmodel import EphemeridesViewModel

router = APIRouter()


SALT_OBSERVATORY_ID = "B31"


@router.post("/ephemerides")
async def ephemerides(request: Request) -> Response:
    vm = EphemeridesViewModel(request)
    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    horizons_service = HorizonsService(
        vm.identifier,
        location=SALT_OBSERVATORY_ID,
        start=vm.start,
        end=vm.end,
        stepsize=vm.output_interval * u.min,
    )
    ephemerides_ = horizons_service.ephemerides()
    return JSONResponse(
        [
            {
                "epoch": e.epoch.timestamp(),
                "ra": e.position.ra.to_value(u.deg),
                "dec": e.position.dec.to_value(u.deg),
                "ra_rate": e.position_rate.ra.to_value(u.arcsec / u.hour),
                "dec_rate": e.position_rate.dec.to_value(u.arcsec / u.hour),
                "magnitude": e.magnitude_range.max_magnitude
                if e.magnitude_range
                else None,
            }
            for e in ephemerides_
        ]
    )
