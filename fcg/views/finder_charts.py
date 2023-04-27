from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from starlette import status

from fcg.viewmodels.hrs_viewmodel import HrsViewModel
from fcg.viewmodels.imaging_viewmodel import ImagingViewModel
from fcg.viewmodels.longslit_viewmodel import LongslitViewModel
from fcg.viewmodels.mos_viewmodel import MosViewModel
from fcg.viewmodels.nir_viewmodel import NirViewModel
from fcg.viewmodels.slotmode_viewmodel import SlotmodeViewModel

router = APIRouter()


@router.post("/finder-charts")
async def generate_finder_chart(request: Request, mode: str) -> Response:
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
            errors = {"__general": f"Unsupported finder chart generation mode: {mode}"}
            return JSONResponse(
                {"errors": errors}, status_code=status.HTTP_400_BAD_REQUEST
            )


async def _hrs(request: Request) -> Response:
    vm = HrsViewModel(request)

    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    return JSONResponse({"success": True})


async def _imaging(request: Request) -> Response:
    vm = ImagingViewModel(request)

    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    return JSONResponse({"success": True})


async def _longslit(request: Request) -> Response:
    vm = LongslitViewModel(request)

    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    return JSONResponse({"success": True})


async def _mos(request: Request) -> Response:
    vm = MosViewModel(request)

    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    return JSONResponse({"success": True})


async def _nir(request: Request) -> Response:
    vm = NirViewModel(request)

    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    return JSONResponse({"success": True})


async def _slotmode(request: Request) -> Response:
    vm = SlotmodeViewModel(request)

    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    return JSONResponse({"success": True})
