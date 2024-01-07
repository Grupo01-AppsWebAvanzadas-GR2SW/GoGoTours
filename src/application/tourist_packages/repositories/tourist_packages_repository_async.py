from abc import ABC, abstractmethod
from src.domain.tourist_packages.entities.tourist_package import TouristPackage
from src.application.common.repositories.generic_repository_async import GenericRepositoryAsync


class TouristPackagesRepositoryAsync(GenericRepositoryAsync[TouristPackage, str], ABC):
    @abstractmethod
    async def get_n_latest_packages(self, n: int) -> list[TouristPackage]:
        pass

    async def list_async(self) -> list[TouristPackage]:
        pass

# TODO: Implementar envio de datos
