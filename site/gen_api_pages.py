from __future__ import annotations

from pathlib import Path

import mkdocs_gen_files

# Which code roots to document
CODE_ROOTS = [
    Path("policyengine"),
    Path("services") / "policyengine_svc",
    Path("agents"),
]

nav = mkdocs_gen_files.Nav()

for root in CODE_ROOTS:
    if not root.exists():
        continue

    for path in sorted(root.rglob("*.py")):
        # Skip dunder modules and tests
        if path.name.startswith("_"):
            continue
        if "tests" in path.parts:
            continue

        # Example: policyengine/engine.py -> policyengine.engine
        module_path = path.with_suffix("").relative_to(".")
        module_parts = list(module_path.parts)
        module_name = ".".join(module_parts)

        # Try to import it; if it fails, skip so mkdocstrings doesn't blow up
        try:
            __import__(module_name)
        except Exception:
            # If you want to see what got skipped, uncomment:
            # print(f"Skipping {module_name} (import failed)")
            continue

        # Actual docs file location: docs/api/policyengine/engine.md, etc.
        doc_path = Path("api", *module_parts).with_suffix(".md")

        # For SUMMARY.md, paths should be relative to docs/api/, e.g. "policyengine/engine.md"
        rel_nav_path = Path(*module_parts).with_suffix(".md")

        nav[module_name] = rel_nav_path.as_posix()

        with mkdocs_gen_files.open(doc_path, "w") as fd:
            print(f"# `{module_name}`", file=fd)
            print("", file=fd)
            print(f"::: {module_name}", file=fd)

# Generate literate-nav file for the whole API section
nav_path = Path("api", "SUMMARY.md")
with mkdocs_gen_files.open(nav_path, "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
