import pytest
from unittest.mock import MagicMock, patch
from kubernetes.client.exceptions import ApiException
from src.integrations.k8s_client import KubernetesClient

@pytest.fixture
def mock_k8s():
    with patch("kubernetes.config.load_kube_config"), \
         patch("kubernetes.client.CoreV1Api") as mock_core_v1:
        yield mock_core_v1.return_value

def test_list_problem_pods(mock_k8s):
    mock_k8s.list_pod_for_all_namespaces.return_value.items = [
        MagicMock(metadata=MagicMock(name="pod1"), status=MagicMock(phase="CrashLoopBackOff")),
        MagicMock(metadata=MagicMock(name="pod2"), status=MagicMock(phase="Running"))
    ]
    k8s = KubernetesClient()
    problem_pods = k8s.list_problem_pods()
    assert len(problem_pods) == 1
    assert problem_pods[0].metadata.name == "pod1"

def test_restart_pod(mock_k8s):
    k8s = KubernetesClient()
    k8s.restart_pod("pod1", "default")
    mock_k8s.delete_namespaced_pod.assert_called_once()

def test_restart_pod_not_found(mock_k8s):
    mock_k8s.delete_namespaced_pod.side_effect = ApiException(status=404)
    k8s = KubernetesClient()
    with pytest.raises(Exception):
        k8s.restart_pod("nonexistent-pod", "default")