import platform
from opentelemetry.sdk.resources import Resource
from baselime.opentelemetry.options import BaselimeOptions


def create_resource(options: BaselimeOptions):
    attributes = {
        "service.name": options.service_name,
        "baselime.distro.runtime_version": platform.python_version()
    }
    if options.service_version:
        attributes["service.version"] = options.service_version
    return Resource.create(attributes)