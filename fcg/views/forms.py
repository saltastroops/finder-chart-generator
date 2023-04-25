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


@router.post("/hrs")
async def hrs(request: Request) -> Response:
    vm = HrsViewModel(request)

    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    return JSONResponse({"success": True})


@router.post("/imaging")
async def hrs(request: Request) -> Response:
    vm = ImagingViewModel(request)

    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    return JSONResponse({"success": True})


@router.post("/longslit")
async def longslit(request: Request) -> Response:
    vm = LongslitViewModel(request)

    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    return JSONResponse({"success": True})


@router.post("/mos")
async def mos(request: Request) -> Response:
    vm = MosViewModel(request)

    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    return JSONResponse({"success": True})


@router.post("/nir")
async def mos(request: Request) -> Response:
    vm = NirViewModel(request)

    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    return JSONResponse({"success": True})


@router.post("/slotmode")
async def slotmode(request: Request) -> Response:
    vm = SlotmodeViewModel(request)

    await vm.load()

    if len(vm.errors) > 0:
        return JSONResponse(
            {"errors": vm.errors}, status_code=status.HTTP_400_BAD_REQUEST
        )

    return JSONResponse({"success": True})
