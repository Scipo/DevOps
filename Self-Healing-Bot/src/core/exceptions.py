class KubernetesConnectionError(Exception):
    """Raised when unable to connect to Kubernetes"""

class PodNotFoundError(Exception):
    """Raised when a pod is not found"""

class PolicyViolationError(Exception):
    """Raised when a healing policy is violated"""
