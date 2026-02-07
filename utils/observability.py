import os
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# Optional GCP exporter
try:
    from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
    GCP_AVAILABLE = True
except:
    GCP_AVAILABLE = False


def setup_tracing():
    resource = Resource.create({
        "service.name": "leave-policy-agent",
    })

    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    # Console exporter (always works locally)
    console_exporter = ConsoleSpanExporter()
    provider.add_span_processor(
        BatchSpanProcessor(console_exporter)
    )

    # GCP exporter (only if project set)
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if GCP_AVAILABLE and project_id:
        gcp_exporter = CloudTraceSpanExporter(
            project_id=project_id
        )

        provider.add_span_processor(
            BatchSpanProcessor(gcp_exporter)
        )


def get_tracer(name: str = __name__):
    return trace.get_tracer(name)
