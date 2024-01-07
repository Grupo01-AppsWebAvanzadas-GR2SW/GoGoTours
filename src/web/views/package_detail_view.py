from flask import render_template, request, redirect, url_for
from flask.views import MethodView
from injector import inject
from src.application.tourist_packages.services.tourist_packages_service_async import TouristPackagesServiceAsync


class PackageDetailView(MethodView):

    @inject
    def __init__(self, tourist_packages_service: TouristPackagesServiceAsync):
        self._tourist_packages_service = tourist_packages_service

    async def get(self, name):
        package = await self._tourist_packages_service.get_tourist_package_by_name(name)
        print(package)
        return render_template("home/package_detail.html", package=package)
