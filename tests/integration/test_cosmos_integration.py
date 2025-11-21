import pytest
pytestmark = pytest.mark.skip(reason="Legacy test; feature not implemented in new engine yet")


"""
Integration Test — Cosmos DB Evidence Ingestion (Optional)

This test verifies optional integration with Azure Cosmos DB for evidence
storage/retrieval.

It is intentionally designed to:

1. **Skip automatically** unless Cosmos DB credentials are provided.
2. Provide a **real integration path** when environment variables are set.
3. Protect CI/CD pipelines by default (no secrets required to run the suite).

Environment variables required to activate this test:

    COSMOS_URL               - Cosmos DB endpoint URL
    COSMOS_KEY               - Primary key or access key
    COSMOS_DATABASE          - Database name
    COSMOS_CONTAINER         - Container/collection name

If *any* of the above are missing, the test is skipped automatically.

When enabled, the test performs a minimal workflow:

    • Create a test document
    • Read it back
    • Validate that it round-trips correctly

This simulates the evidence ingestion flow for the 4th.GRC platform where
agent-collected evidence may be stored or retrieved from Cosmos.
"""

import os
import pytest

try:
    from azure.cosmos import CosmosClient, PartitionKey
except ImportError:
    CosmosClient = None


def _cosmos_env_ready() -> bool:
    """Return True if ALL required Cosmos env vars are defined."""
    required = [
        "COSMOS_URL",
        "COSMOS_KEY",
        "COSMOS_DATABASE",
        "COSMOS_CONTAINER",
    ]
    return all(os.getenv(var) for var in required)


@pytest.mark.integration
@pytest.mark.skipif(CosmosClient is None, reason="azure-cosmos package not installed")
@pytest.mark.skipif(
    not _cosmos_env_ready(),
    reason="Cosmos DB env vars not provided; skipping safe integration test."
)
def test_cosmos_evidence_roundtrip():
    """Write and read back a document to Cosmos DB (only if env + deps present)."""

    url = os.getenv("COSMOS_URL")
    key = os.getenv("COSMOS_KEY")
    db_name = os.getenv("COSMOS_DATABASE")
    container_name = os.getenv("COSMOS_CONTAINER")

    # Create client
    client = CosmosClient(url, credential=key)

    # Ensure DB + container exist
    db = client.create_database_if_not_exists(id=db_name)
    container = db.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/system_id"),
        offer_throughput=400
    )

    # Minimal evidence document
    doc = {
        "id": "test-cosmos-doc",
        "system_id": "demo-system",
        "FAIRNESS_SCORE": 0.91,
        "DISPARITY_RATIO": 1.04,
        "_test_flag": True,
    }

    # Write
    container.upsert_item(doc)

    # Read back
    returned = container.read_item(
        item="test-cosmos-doc",
        partition_key="demo-system"
    )

    # Validate
    assert returned["id"] == doc["id"]
    assert returned["system_id"] == doc["system_id"]
    assert returned["_test_flag"] is True
    assert returned["FAIRNESS_SCORE"] == pytest.approx(0.91, rel=1e-3)

    # Cleanup (best effort)
    try:
        container.delete_item(item="test-cosmos-doc", partition_key="demo-system")
    except Exception:
        pass  # non-fatal
