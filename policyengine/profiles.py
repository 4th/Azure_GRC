from __future__ import annotations

from pathlib import Path
from typing import Dict

import yaml

from .schema import PolicyProfile
from .exceptions import ProfileNotFoundError

ROOT_DIR = Path(__file__).resolve().parents[1]
PROFILES_DIR = ROOT_DIR / "profiles"


def load_profile_by_ref(profile_ref: str) -> PolicyProfile:
    """
    Load a profile by 'profile_ref', currently assumed to be:
      profile_id@version  (e.g. iso_42001-global@1.2.0)

    For now we map profile_ref -> file name "<profile_id>.yaml".
    You can change this strategy later as needed.
    """
    if "@" in profile_ref:
        profile_id, version = profile_ref.split("@", 1)
    else:
        profile_id = profile_ref
        version = "latest"

    path = PROFILES_DIR / f"{profile_id}.yaml"
    if not path.exists():
        raise ProfileNotFoundError(f"Profile file not found for id: {profile_id}")

    data: Dict = yaml.safe_load(path.read_text(encoding="utf-8"))
    profile = PolicyProfile.model_validate(data)

    if version != "latest" and profile.version != version:
        raise ProfileNotFoundError(
            f"Requested version {version}, but profile file has version {profile.version}"
        )

    return profile
