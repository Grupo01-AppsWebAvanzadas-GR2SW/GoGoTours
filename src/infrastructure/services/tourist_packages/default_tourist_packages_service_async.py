from datetime import datetime
from src.domain.tourist_packages.entities.tourist_package import TouristPackage
from src.application.tourist_packages.services.tourist_packages_service_async import TouristPackagesServiceAsync
from src.application.tourist_packages.dtos.tourist_packages_response_dto import TouristPackagesResponseDto
from src.application.tourist_packages.dtos.tourist_packages_request_dto import TouristPackagesRequestDto
from src.application.tourist_packages.repositories.tourist_packages_repository_async import \
    TouristPackagesRepositoryAsync
from injector import inject


class DefaultTouristPackagesServiceAsync(TouristPackagesServiceAsync):
    @inject
    def __init__(self, tourist_packages_repository_async: TouristPackagesRepositoryAsync):
        self._tourist_packages_repository_async = tourist_packages_repository_async

    async def get_tourist_packages(self) -> list[TouristPackagesResponseDto]:
        packages = await self._tourist_packages_repository_async.list_async()

        return [TouristPackagesResponseDto(
            id=package.id,
            name=package.name,
            description=package.description,
            destination_place=package.destination_place,
            duration=package.duration,
            max_capacity=package.max_capacity,
            cost=package.cost,
            start_date=package.start_date,
            end_date=package.end_date,
            image=package.image
        ) for package in packages]

    async def get_tourist_package_by_name(self, name: str) -> TouristPackagesResponseDto:
        package = await self._tourist_packages_repository_async.get_by_name_async(name)

        return TouristPackagesResponseDto(
            id=package.id,
            name=package.name,
            description=package.description,
            destination_place=package.destination_place,
            duration=package.duration,
            max_capacity=package.max_capacity,
            cost=package.cost,
            start_date=package.start_date,
            end_date=package.end_date,
            image=package.image
        )

    async def add_package(self, tourist_package: TouristPackagesResponseDto):
        await self._tourist_packages_repository_async.add_async(
            TouristPackage(
                name=tourist_package.name,
                description=tourist_package.description,
                destination_place=tourist_package.destination_place,
                duration=tourist_package.duration,
                max_capacity=tourist_package.max_capacity,
                cost=tourist_package.cost,
                start_date=tourist_package.start_date,
                end_date=tourist_package.end_date,
                image=tourist_package.image
            )
        )

    async def edit_package(self, name: str, updated_package: TouristPackagesRequestDto):
        package = await self._tourist_packages_repository_async.get_by_name_async(name)

        if package:
            # Actualiza los campos del paquete con los valores proporcionados en updated_package
            package.name = updated_package.name
            package.description = updated_package.description
            package.destination_place = updated_package.destination_place
            package.duration = updated_package.duration
            package.max_capacity = updated_package.max_capacity
            package.cost = updated_package.cost
            package.start_date = updated_package.start_date
            package.end_date = updated_package.end_date
            package.image = updated_package.image

            await self._tourist_packages_repository_async.update_async(package)
            return True
        else:
            return False