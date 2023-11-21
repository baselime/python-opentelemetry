from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SimpleSpanProcessor,
    ConsoleSpanExporter
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as GRPCSpanExporter
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as HTTPSpanExporter
)

from baselime.opentelemetry.options import BaselimeOptions
from baselime.opentelemetry.baggage import BaggageSpanProcessor


def create_tracer_provider(
    options: BaselimeOptions,
    resource: Resource
) -> TracerProvider:
    """
    Configures and returns a new TracerProvider to send traces telemetry.

    Args:
        options (BaselimeOptions): the Baselime options to configure with
        resource (Resource): the resource to use with the new tracer provider

    Returns:
        TracerProvider: the new tracer provider
    """

    exporter = HTTPSpanExporter(
        endpoint=options.get_traces_endpoint(),
        headers=options.get_trace_headers()
    )
    trace_provider = TracerProvider(
        resource=resource,
    )
    trace_provider.add_span_processor(
        BaggageSpanProcessor()
    )

    trace_provider.add_span_processor(
        SimpleSpanProcessor(
            exporter
        )
    )
    if options.debug:
        trace_provider.add_span_processor(
            SimpleSpanProcessor(
                ConsoleSpanExporter()
            )
        )
    return trace_provider