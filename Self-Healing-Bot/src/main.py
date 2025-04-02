import logging
import logging.config
import time
from dotenv import load_dotenv
from src.integrations.k8s_client import KubernetesClient
from src.integrations.metrics_service import HealingMetrics


load_dotenv("config/.env")

logging.config.fileConfig("config/logging.conf")
logger = logging.getLogger(__name__)

class HealingBot:
    def __init__(self):
        self.k8s = KubernetesClient()
        self.metric = HealingMetrics()

    def run(self, interval: int = 60):
        """Main healing loop."""
        logger.info("Starting Healing Bot...")
        while True:
            try:
                self._check_and_heal_pods()
            except Exception as e:
                logger.error(f"Healing cycle failed: {e}")
            time.sleep(interval)

    def _check_and_heal_pods(self):
        """Check for problem pods and restart them."""
        pods = self.k8s.list_problem_pods()
        self.metric.update_problem_pods(len(pods))

        if not pods:
            logger.debug("No problematic pods found.")
            return
        logger.warning(f"Found {len(pods)} problematic pods.")
        for pod in pods:
            try:
                self.k8s.restart_pod(pod.metadata.name, pod.metadata.namespace)
                self.metric.increment_restart(pod.metadata.namespace)
            except Exception as e:
                self.metric.record_error(type(e).__name__)
                logger.error(f"Failed to restart pod {pod.metadata.name}: {e}")


if __name__ == "__main__":
    bot = HealingBot()
    bot.run()
