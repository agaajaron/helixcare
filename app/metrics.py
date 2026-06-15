
from prometheus_client import Counter, Histogram, start_http_server
import threading

REQUESTS = Counter('caregraph_requests_total', 'Total requests', ['flow'])
ERRORS = Counter('caregraph_errors_total', 'Total errors', ['type'])
CITATIONS = Counter('caregraph_citations_total', 'Citations detected')
MISSING_CITATIONS = Counter('caregraph_missing_citations_total', 'Missing citations')
LATENCY = Histogram('caregraph_request_latency_seconds', 'Request latency', ['flow'])

_started = False
_lock = threading.Lock()

def ensure_metrics_server(port: int = 9000):
    global _started
    if _started:
        return
    with _lock:
        if not _started:
            start_http_server(port)
            _started = True
