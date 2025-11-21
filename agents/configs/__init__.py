"""
agents.configs

Configuration utilities for the 4th.GRC agentic toolkit.

This package currently includes:

- `agent_profiles.yaml` – model, tool, and policy configuration for agents.

You can optionally add Python helpers here later, for example:

    from pathlib import Path
    import yaml

    def load_agent_profiles(path: str | Path | None = None) -> dict:
        base = Path(__file__).resolve().parents[1]
        default_path = base / "configs" / "agent_profiles.yaml"
        with (Path(path) if path else default_path).open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)

For now, this module simply marks `agents.configs` as a package.
"""

from __future__ import annotations

__all__: list[str] = []
