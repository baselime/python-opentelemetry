# Python Baselime OpenTelemetry SDK
[![Documentation][docs_badge]][docs]
[![Latest Release][release_badge]][release]
[![License][license_badge]][license]

Instrument your Python applications with OpenTelemetry and send the traces to [Baselime](https://baselime.io)

## Getting Started 

Check out the [documentation](https://baselime.io/docs/sending-data/opentelemetry/).

## Example

```bash
poetry add baselime-opentelemetry

BASELIME_API_KEY=<YOUR_API_KEY> poetry run opentelemetry-instrument python myapp.py
```