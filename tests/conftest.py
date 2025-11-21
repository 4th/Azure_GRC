from __future__ import annotations

from pathlib import Path
from typing import Dict, Any
import sys

import pytest
from fastapi.testclient import TestClient

# --- Make sure project root (C:\4th\4th.GRC) is on sys.path ---
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Now this import should work:
from services.policyengine_svc.main import app


# ---------- Path fixtures ----------

@pytest.fixture(scope="session")
def tests_root() -> Path:
    return Path(__file__).resolve().parent


@pytest.fixture(scope="session")
def data_dir(tests_root: Path) -> Path:
    return tests_root / "data"


@pytest.fixture(scope="session")
def data_profiles_dir() -> Path:
    """
    Use the *runtime* profiles directory instead of tests/data/profiles.

    This points tests at:
        C:/4th/4th.GRC/profiles
    so they exercise the same profiles that the PolicyEngine service uses.
    """
    return ROOT_DIR / "profiles"


@pytest.fixture(scope="session")
def data_evidence_dir(data_dir: Path) -> Path:
    return data_dir / "evidence"


@pytest.fixture(scope="session")
def data_requests_dir(data_dir: Path) -> Path:
    return data_dir / "requests"


# ---------- Sample data fixtures ----------

@pytest.fixture
def sample_profile_yaml(data_profiles_dir: Path) -> str:
    path = data_profiles_dir / "iso_42001-global.yaml"
    return path.read_text(encoding="utf-8")


@pytest.fixture
def malformed_profile_yaml(data_profiles_dir: Path) -> str:
    path = data_profiles_dir / "malformed.yaml"
    return path.read_text(encoding="utf-8")


@pytest.fixture
def sample_eval_request_dict() -> Dict[str, Any]:
    return {
        "profile_ref": "iso_42001-global@1.2.0",
        "context": {"system_name": "Demo LLM System", "owner": "Test Owner"},
        "evidence": {},
    }


@pytest.fixture
def sample_model_card_json(data_evidence_dir: Path) -> Dict[str, Any]:
    import json

    path = data_evidence_dir / "example_model_card.json"
    return json.loads(path.read_text(encoding="utf-8"))


# ---------- FastAPI client ----------

@pytest.fixture(scope="session")
def api_client() -> TestClient:
    return TestClient(app)
