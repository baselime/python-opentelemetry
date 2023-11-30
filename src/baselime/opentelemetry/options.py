import logging
import os
from opentelemetry.sdk.environment_variables import (
    OTEL_LOG_LEVEL,
    OTEL_SERVICE_NAME
)

# Environment Variable Names
OTEL_SERVICE_VERSION = "OTEL_SERVICE_VERSION"
DEBUG = "DEBUG"
EXPORT_CONSOLE = "EXPORT_CONSOLE"
SAMPLE_RATE = "SAMPLE_RATE"
BASELIME_API_KEY = "BASELIME_API_KEY"
BASELIME_URL = "BASELIME_URL"
# Default values
DEFAULT_API_ENDPOINT = "https://otel.baselime.io/v1"
DEFAULT_SERVICE_NAME = "unknown_service:python"
DEFAULT_LOG_LEVEL = "ERROR"

# Errors and Warnings
INVALID_DEBUG_ERROR = "Unable to parse DEBUG environment variable. " + \
    "Defaulting to False."
INVALID_EXPORTER_PROTOCOL_ERROR = "Invalid OTLP exporter protocol " + \
    "detected. Must be one of ['grpc', 'http/protobuf']. Defaulting to grpc."
MISSING_API_KEY_ERROR = "Missing API key. Specify either " + \
    "BASELIME_API_KEY environment variable or apikey in the options" + \
    "parameter."
MISSING_SERVICE_NAME_ERROR = "Missing service name. Specify either " + \
    "OTEL_SERVICE_NAME environment variable or service_name in the " + \
    "options parameter. If left unset, this will show up in BASELIME " + \
    "as unknown_service:python"

# not currently supported in OTel SDK, open PR:
# https://github.com/open-telemetry/opentelemetry-specification/issues/1901

log_levels = {
    "NOTSET": logging.NOTSET,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

_logger = logging.getLogger('baselime.opentelemetry.options')



def parse_bool(environment_variable: str,
               default_value: bool,
               error_message: str) -> bool:
    """
    Attempts to parse the provided environment variable into a bool. If it
    does not exist or fails parse, the default value is returned instead.

    Args:
        environment_variable (str): the environment variable name to use
        default_value (bool): the default value if not found or unable parse
        error_message (str): the error message to log if unable to parse

    Returns:
        bool: either the parsed environment variable or default value
    """
    val = os.getenv(environment_variable, None)
    if val:
        try:
            return bool(val)
        except ValueError:
            _logger.warning(error_message)
    return default_value

class BaselimeOptions:
    """
    Baselime Options used to configure the OpenTelemetry SDK.

    Setting the debug flag TRUE enables verbose logging and sets the
    OTEL_LOG_LEVEL to DEBUG.

    An option set as an environment variable will override any existing
    options declared as parameter variables, if neither are present it
    will fall back to the default value.

    Defaults are declared at the top of this file, i.e. DEFAULT_SAMPLE_RATE = 1
    """
    service_name = DEFAULT_SERVICE_NAME
    endpoint = DEFAULT_API_ENDPOINT
    debug = False
    log_level = DEFAULT_LOG_LEVEL
    export_console = False
    def __init__(
        self,
        apikey: str = None,
        service_name: str = None,
        service_version: str = None,
        endpoint: str = None,
        debug: bool = False,
        log_level: str = None,
    ):
        self.debug = parse_bool(
            DEBUG,
            (debug or False),
            INVALID_DEBUG_ERROR
        )
        if self.debug:
            self.log_level = "DEBUG"
        else:
            log_level = os.environ.get(OTEL_LOG_LEVEL, log_level)
            if log_level and log_level.upper() in log_levels:
                self.log_level = log_level.upper()
        logging.basicConfig(level=log_levels[self.log_level])

        self.export_console = os.environ.get(EXPORT_CONSOLE, False)
        
        self.api_key = os.environ.get(
            BASELIME_API_KEY,
            os.environ.get(
                BASELIME_API_KEY,
                apikey
            )
        )
        if not self.api_key:
            _logger.warning(MISSING_API_KEY_ERROR)


        self.service_name = os.environ.get(OTEL_SERVICE_NAME, service_name)
        if not self.service_name:
            _logger.warning(MISSING_SERVICE_NAME_ERROR)
            self.service_name = DEFAULT_SERVICE_NAME
        self.service_version = os.environ.get(
            OTEL_SERVICE_VERSION, service_version)


        self.endpoint = os.environ.get(
            BASELIME_URL,
            endpoint
        )

        if not self.endpoint:
            self.endpoint = DEFAULT_API_ENDPOINT
    def get_traces_endpoint(self) -> str:
        """
        Returns the OTLP traces endpoint to send spans to.
        """
        return self.endpoint
    def get_trace_headers(self):
        """
        Gets the headers to send traces telemetry.
        """
        headers = {
            "x-api-key": self.api_key,
        }

        return headers
