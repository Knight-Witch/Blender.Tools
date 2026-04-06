# CHANGELOG

## v0.1.0-dev1 — License correction
Date: 2026-04-06

Purpose:
- Replace the default MIT-style open-source license with a restrictive proprietary license aligned with the project owner’s intent.
- Update the public README so repository usage restrictions are visible immediately.

Changed:
- Removed root `LICENSE` file containing MIT terms.
- Added root `LICENSE.md` with all-rights-reserved proprietary terms.
- Added a copyright / usage notice near the top of `README.md`.

Rollback guidance:
- If needed, restore the previous scaffold zip.
- This release should be treated as the correct licensing baseline going forward.

## v0.1.0-dev0 — Initial scaffold baseline
Date: 2026-04-06

Purpose:
- Establish the repo/package layout for Witch Bones.
- Create a rollback-friendly baseline before real implementation begins.
- Separate the addon into subsystem modules instead of one monolithic script.

Added:
- `README.md`
- `docs/WITCH_BONES_MASTER_SPEC.md`
- `docs/WITCH_BONES_IMPLEMENTATION_SPEC.md`
- `docs/WITCH_BONES_PROFILE_SCHEMA.md`
- `dev/test_assets_manifest.md`
- `dev/sample_notes.md`
- `witch_bones/` addon package scaffold
- `witch_bones/data/profiles/ova_profile.json`

Package modules added:
- `__init__.py`
- `constants.py`
- `registration.py`
- `preferences.py`
- `properties.py`
- `session.py`
- `profiles.py`
- `backup.py`
- `detect.py`
- `helper_clone.py`
- `commit.py`
- `mapping.py`
- `weights.py`
- `rename.py`
- `bg3.py`
- `cleanup.py`
- `logging_utils.py`
- `ui.py`
- `operators_preflight.py`
- `operators_backup.py`
- `operators_filter.py`
- `operators_helper.py`
- `operators_pipeline.py`
- `operators_restore.py`

Rollback guidance:
- This version is the clean baseline scaffold.
- If a later drop breaks the addon, restore this full package snapshot first.
- Future releases should append new changelog entries rather than replacing prior entries.

Update policy:
- Milestone drops should be delivered as full package zips.
- Small hotfixes can be delivered as overwrite zips containing only changed files.
- Every release should append a dated entry here and update each changed file header.
