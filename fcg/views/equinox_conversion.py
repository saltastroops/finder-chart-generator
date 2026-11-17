from astropy import units as u
from astropy.coordinates import FK5, SkyCoord
from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from fcg.viewmodels.equinox_conversion_viewmodel import EquinoxConversionViewModel

router = APIRouter()


@router.get("/equinox-conversion")
async def convert_equinox(request: Request) -> Response:
    vm = EquinoxConversionViewModel(request)
    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    old_frame = FK5(equinox=f"J{vm.old_equinox}")
    new_frame = FK5(equinox=f"J{vm.new_equinox}")
    old_coordinates = SkyCoord(ra=vm.right_ascension, dec=vm.declination, frame=old_frame)
    new_coordinates = old_coordinates.transform_to(new_frame)

    right_ascension = new_coordinates.ra.to(1 * u.deg).to_value()
    declination = new_coordinates.dec.to(1 * u.deg).to_value()

    return JSONResponse({"right_ascension": right_ascension, "declination": declination, "equinox": vm.new_equinox})
