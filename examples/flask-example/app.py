from flask import Flask
from opentelemetry.trace import get_tracer
from opentelemetry.instrumentation.flask import FlaskInstrumentor
app = Flask(__name__)


FlaskInstrumentor().instrument_app(app)

tracer = get_tracer(__name__)
@app.route('/')
def hello_world():
    with tracer.start_as_current_span('hello'):
        with tracer.start_as_current_span('world'):
            with tracer.start_as_current_span('!'):
                return 'Hello, OpenTelemetry!'