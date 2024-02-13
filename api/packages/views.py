from typing import List


from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.middleware.session import session_middleware
from api.packages.crud import ShippingCostState
from models import db_helper
from api.packages.schemas import Package, PackageResponse, PackageType, PackageUpdate
from api.packages import crud
from price_updater.celery_worker import update

router = APIRouter(tags=["Packages"])


@router.post("/register_package", response_model=PackageResponse)
async def register_package(
    package: Package,
    session_id: str = Depends(session_middleware.get_current_session_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    new_package = await crud.register_package(
        user_session_id=session_id, package_in=package, session=session
    )
    package_register_response = PackageResponse(
        message="Посылка успешно зарегистрирована",
        id=new_package.id,
    )
    return package_register_response


@router.get("/package_types", response_model=List[PackageType])
async def get_all_package_types(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_all_package_types(session=session)


@router.get("/packages", response_model=List[PackageUpdate])
async def get_user_packages(
    limit: int = 10,
    offset: int = 0,
    sc_filter: ShippingCostState | None = None,
    session_id: str = Depends(session_middleware.get_current_session_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_user_packages(
        session=session,
        user_session_id=session_id,
        shipping_cost_filter=sc_filter,
        limit=limit,
        offset=offset,
    )


@router.get("/packages/{package_id}", response_model=PackageUpdate)
async def get_package_by_id(
    package_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_package_by_id(package_id_in=package_id, session=session)


@router.post("/force-run-shipping_cost_update/")
async def force_run_cost_update():
    await update()
    return {"message": f"Periodic shipping_cost_update was forcefully run."}
