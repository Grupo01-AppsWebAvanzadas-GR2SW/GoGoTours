from abc import ABC, abstractmethod
from src.domain.tourist_packages.entities.tourist_package import TouristPackage
from src.application.tourist_packages.dtos.tourist_packages_response_dto import TouristPackagesResponseDto


class TouristPackagesServiceAsync(ABC):
    @abstractmethod
    async def get_tourist_packages(self) -> list[TouristPackagesResponseDto]:
        pass

    @abstractmethod
    async def get_tourist_package_by_name(self, name: str) -> TouristPackagesResponseDto:
        pass
