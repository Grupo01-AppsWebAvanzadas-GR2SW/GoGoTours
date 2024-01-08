from flask import render_template, request, redirect, url_for
from flask.views import MethodView
from injector import inject
from src.application.tourist_packages.services.tourist_packages_service_async import TouristPackagesServiceAsync
from src.application.tourist_packages.dtos.tourist_packages_request_dto import TouristPackagesRequestDto


class PackageAddView(MethodView):
    @inject
    def __init__(self, tourist_packages_service: TouristPackagesServiceAsync):
        self._tourist_packages_service = tourist_packages_service

    async def get(self):
        packages = await self._tourist_packages_service.get_tourist_packages()
        return render_template("packagesManager/add_Package.html", packages=packages)

    async def post(self):
        print(request.form.get("packageName"))
        package_name = request.form.get("packageName")
        package_description = request.form.get("packageDescription")
        package_destination = request.form.get("packageDestinationPlace")
        package_duration = request.form.get("packageDuration")
        package_capacity = request.form.get("packageMaxCapacity")
        package_cost = request.form.get("packageCost")
        package_start_Date = request.form.get("packageStateDate")
        package_end_Date = request.form.get("packageEndDate")

        package_dto = TouristPackagesRequestDto(
            name=package_name,
            description=package_description,
            destination_place=package_destination,
            duration=package_duration,
            max_capacity=package_capacity,
            cost=package_cost,
            start_date=package_start_Date,
            end_date=package_end_Date

        )
        await self._tourist_packages_service.add_package(package_dto)
        return redirect(url_for("home"))
