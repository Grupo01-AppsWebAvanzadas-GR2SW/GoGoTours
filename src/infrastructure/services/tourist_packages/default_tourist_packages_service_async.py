from datetime import datetime
from src.domain.tourist_packages.entities.tourist_package import TouristPackage
from src.application.tourist_packages.services.tourist_packages_service_async import TouristPackagesServiceAsync
from src.application.tourist_packages.dtos.tourist_packages_response_dto import TouristPackagesResponseDto
from src.application.tourist_packages.repositories.tourist_packages_repository_async import TouristPackagesRepositoryAsync
from injector import inject


class DefaultTouristPackagesServiceAsync(TouristPackagesServiceAsync):
    @inject
    def __init__(self, tourist_packages_repository_async: TouristPackagesRepositoryAsync):
        self._tourist_packages_repository_async = tourist_packages_repository_async

    async def get_tourist_packages(self) -> list[TouristPackagesResponseDto]:
        packages = await self._tourist_packages_repository_async.list_async()

        return [TouristPackagesResponseDto(
            name=package.name,
            description=package.description,
            destination_place=package.destination_place,
            duration=package.duration,
            max_capacity=package.max_capacity,
            cost=package.cost,
            start_date=package.start_date,
            end_date=package.end_date
        ) for package in packages]

    async def get_tourist_package_by_name(self, name: str) -> TouristPackagesResponseDto:
        package = await self._tourist_packages_repository_async.get_by_name_async(name)

        return TouristPackagesResponseDto(
            name=package.name,
            description=package.description,
            destination_place=package.destination_place,
            duration=package.duration,
            max_capacity=package.max_capacity,
            cost=package.cost,
            start_date=package.start_date,
            end_date=package.end_date
        )