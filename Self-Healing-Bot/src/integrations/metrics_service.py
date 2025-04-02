from prometheus_client import start_http_server, Counter, Gauge

import logging

logger = logging.getLogger(__name__)

class HealingMetrics:
    def __init__(self, port = 9000):
        start_http_server(port)
        self.pods_restarted = Counter(
            'healing_bot_pods_restarted_total',
            'Total pods restarted by healing bot',
            ['namespace']
        )
        self.errors_total = Counter(
            'healing_bot_errors_total',
            'Total errors encountered',
            ['error_type']
        )
        self.current_problem_pods = Gauge(
            'healing_bot_problem_pods_current',
            'Current count of problematic pods'
        )
    def increment_restart(self, namespace):
        self.pods_restarted.labels(namespace = namespace).inc()
    def record_error(self, error_type):
        self.errors_total.labels(error_type=error_type).inc()
    def update_problem_pods(self, count):
        self.current_problem_pods.set(count)