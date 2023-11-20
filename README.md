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

## License

&copy; Baselime Limited, 2023

Distributed under MIT License (`The MIT License`).

See [LICENSE](LICENSE) for more information.

<!-- Badges -->

[docs]: https://baselime.io/docs/
[docs_badge]: https://img.shields.io/badge/docs-reference-blue.svg?style=flat-square
[release]: https://github.com/baselime/node-opentelemetry/releases/latest
[release_badge]: https://img.shields.io/github/release/baselime/node-opentelemetry.svg?style=flat-square&ghcache=unused
[license]: https://opensource.org/licenses/MIT
[license_badge]: https://img.shields.io/github/license/baselime/node-opentelemetry.svg?color=blue&style=flat-square&ghcache=unused