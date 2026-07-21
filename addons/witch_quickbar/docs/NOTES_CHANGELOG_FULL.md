# Witch Quickbar Notes Changelog — Full History

## 2026-07-20 — Development baseline audit

- Recorded user-supplied `Witch Quickbar Dev_v1.3.18` as the best available candidate current dev baseline.
- Recorded artifact `witch_quickbar_dev_Dev_v1_3_18_package.zip`, package folder `witch_quickbar_dev`, Blender target 4.5.0, and archive SHA-256 `01fc12ee366c6484e209d1ee71519bd1f1ca711d4fc3c2710fec5e20b2ba2a1b`.
- Added a complete source and 31-asset SHA-256 manifest.
- Confirmed archive safety, 12 parseable Python files, and no generated cache files.
- Confirmed the separate dev package/operator namespace intended for side-by-side installation with the public Quickbar.
- Located `UPDATE_URL` at `https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Quick_Access`.
- Confirmed the Check for Updates operator only calls Blender's URL opener and performs no version comparison.
- Confirmed no public branch, URL, package identity, operator ID, or asset path was changed.
- Confirmed no Blender runtime test was performed.

## 2026-07-20 — Documentation architecture and public compatibility protection

- Recorded `Witch_Quick_Access` public branch baseline at commit `13242bf0141c7f539af97b39a4aca6e640c0901c`.
- Recorded public v1.0.2 / internal 1.2.8 correlation and Blender 4.5 metadata.
- Established local overlay and input-preservation rules.
- Added project state and a baseline-recovery/compatibility roadmap.
- Added overlay architecture, input/event, asset, and Witch Tools integration documents.
- Recorded root/package documentation-version mismatch for later audit.
- Recorded known development issues as unverified context pending source import.
- Confirmed no Quickbar source, public branch, URL, package identity, external link, or asset was changed or runtime-tested.
