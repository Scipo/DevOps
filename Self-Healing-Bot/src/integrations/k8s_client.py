import os

from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from src.core.circuit_breaker import CircuitBreaker
from src.core.exceptions import KubernetesConnectionError, PodNotFoundError
import logging

logger = logging.getLogger(__name__)

class KubernetesClient:
    def __init__(self):
        self._configure_k8s()
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()

    @staticmethod
    def _configure_k8s() :
        try:
            if os.getenv("KUBERNETES_SERVICE_HOST"):
                config.load_incluster_config()
            else:
                config.load_kube_config()
        except Exception as e:
            raise KubernetesConnectionError(f"Failed to configure Kubernetes: {e}")

    @CircuitBreaker()
    def list_problem_pods(self):
        """Fetch pods in CrashLoopBackOff or NotReady state"""
        try:
            field_selector = (
                "status.phase!=Running,"
                "status.phase!=Succeeded"
            )
            pods = self.core_v1.list_pod_for_all_namespaces(
                field_selector = field_selector
            ).items()
            return [pod for pod in pods if pod.status.phase in ["CrashLoopBackOff", "NotReady"]]
        except ApiException as e:
            logger.error(f"K8s API error: {e}")
    @CircuitBreaker()
    def restart_pod(self, pod_name: str, namespace: str = "default"):
        """Gracefully delete a pod to trigger recreation."""
        try:
            self.core_v1.delete_namespace(
                name = pod_name,
                namespace = namespace,
                body = client.V1DeleteOptions(),
            )
            logger.info(f"Restarted pod: {namespace}/{pod_name}")
        except ApiException as e:
            if e.status == 404:
                raise PodNotFoundError(f"Pod {pod_name} not found")
            raise

