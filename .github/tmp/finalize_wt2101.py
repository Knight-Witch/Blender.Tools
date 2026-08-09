from pathlib import Path
import ast

ROOT = Path('.')
PKG = ROOT / 'addons/witch_tools/dev/Witch_Tools_Dev'


def append_once(path, marker, text):
    p = ROOT / path
    s = p.read_text(encoding='utf-8')
    if marker not in s:
        p.write_text(s.rstrip() + '\n\n' + text.strip() + '\n', encoding='utf-8')


def prepend_once(path, marker, text):
    p = ROOT / path
    s = p.read_text(encoding='utf-8')
    if marker not in s:
        p.write_text(text.rstrip() + '\n\n' + s, encoding='utf-8')


runtime = '''## Dev_v2.10.1 Blender 4.5 regression addendum

Dev_v2.10.0 user testing confirmed hover highlighting, Magnetic Snap, Inject New Undo/Redo, Paver, Organic, and the tested Organic vertex-merge path. Failures found were: Edge Solo/Branch restricted to one edge; only one magnetic contact merged; an old unsplit target edge remained through an inserted vertex; Magic Branch reset the view pivot while waiting; no explicit Magic Branch ON/OFF; no Z-wall Paver growth from a horizontal source; Paver return-path overlaps did not all merge; Branch Type did not synchronize Blender Vertex/Edge/Face selection mode; Object Snap did not enter Undo history.

Dev_v2.10.1 implements source fixes for those cases. Blender 4.5 runtime retest remains required.'''

for path in (
    'addons/witch_tools/docs/features/precision_edit/SPEC.md',
    'addons/witch_tools/docs/features/precision_edit/STATE.md',
    'addons/witch_tools/docs/features/precision_edit/ROADMAP.md',
    'addons/witch_tools/docs/features/magic_branch/SPEC.md',
    'addons/witch_tools/docs/features/magic_branch/STATE.md',
    'addons/witch_tools/docs/features/magic_branch/ROADMAP.md',
):
    append_once(path, '## Dev_v2.10.1 Blender 4.5 regression addendum', runtime)

append_once('addons/witch_tools/docs/features/precision_edit/DECISIONS.md', '## Dev_v2.10.1 runtime decisions', '''## Dev_v2.10.1 runtime decisions

- Merge correctness is commit-wide: hover chooses placement, not the only eligible merge contact.
- A created vertex landing inside an existing edge must split that exact edge before welding; coincident unsplit topology is not acceptable.
- Edge Solo/Branch accepts a rigid set of one or more selected edges while preserving shared source connectivity.
- Only plain MMB during a live drag may assign the live injection pivot. Modifier MMB remains Blender navigation.
- Object Snap uses an explicit Undo boundary candidate because automatic operator Undo did not register reliably in the Blender 4.5 user pass.''')

append_once('addons/witch_tools/docs/features/magic_branch/DECISIONS.md', '## Dev_v2.10.1 runtime decisions', '''## Dev_v2.10.1 runtime decisions

- Magic Branch Active and Persistent are separate: Active controls whether the modal tool runs; Persistent only controls stay-armed behavior after a commit.
- Branch Type buttons request the corresponding Blender mesh selection mode through an undoable operator candidate.
- If the source-plane Paver direction is removed by the enabled axis mask, use the enabled mouse-projected direction while preserving source tile depth; reject a direction parallel to the emitting edge.
- Paver/Organic Auto-Merge checks every supported created overlap at commit, not only the hovered element.''')

regression = '''## Dev_v2.10.1 regression block

1. Edge Solo/Branch: test multiple connected and disconnected selected source edges; the set must duplicate/move rigidly.
2. Move one branched edge so its two new endpoints land on two different target rails while only one rail is hovered. Both contacts must integrate.
3. Interior target-edge contacts must replace the old spanning edge with two segments sharing the inserted/welded vertex; no stale full edge may remain.
4. Test coincident vertex contacts, multiple contacts on one edge, and contacts on different edges. Check zero/duplicate geometry, normals/winding, material/edge attributes, Undo/Redo and cancel rollback.
5. Magic Branch waiting state: Shift+MMB pan and ordinary orbit must not snap the view back to the current selection.
6. During a live branch/injection, plain MMB must orbit around live geometry; modifier MMB must retain normal Blender navigation.
7. Magic Branch ON/OFF must actually enter/exit the modal tool. Persistent OFF exits after one branch; Persistent ON stays armed.
8. Branch Type Vertex/Edge/Face must switch Blender mesh selection mode; test Undo restoration.
9. Horizontal face + Z-only Paver must create vertical source-depth tiles with correct winding and no zero-area faces.
10. Pave +X, +Y, then -X back onto existing topology with Auto-Merge ON. Every supported overlap must integrate and interior edge contacts must subdivide the existing edge.
11. Object Snap Vertex/Edge/Face in object/island scopes must Undo and Redo in one coherent step.'''
append_once('addons/witch_tools/docs/features/precision_edit/TEST_PLAN.md', '## Dev_v2.10.1 regression block', regression)
append_once('addons/witch_tools/docs/features/magic_branch/TEST_PLAN.md', '## Dev_v2.10.1 regression block', regression)

append_once('addons/witch_tools/docs/UI_MAP.md', '## Dev_v2.10.1 UI corrections', '''## Dev_v2.10.1 UI corrections

- Inject New Edge Solo/Branch accepts one or more Edge sources.
- Magic Branch Step 1 now has explicit ON/OFF; Persistent is only stay-armed behavior.
- Magic Branch Branch Type buttons also switch Blender Vertex/Edge/Face selection mode.
- Plain MMB changes the live pivot only while dragging; modifier MMB keeps normal viewport navigation.
- Paver can grow along an enabled out-of-plane axis, including the Z-only floor-to-wall case.''')

append_once('addons/witch_tools/docs/ROADMAP.md', '## Dev_v2.10.1 runtime correction pass', '''## Dev_v2.10.1 runtime correction pass — active

Multi-edge Edge Solo/Branch, commit-wide overlap integration with true target-edge subdivision, Magic Branch navigation/ON-OFF/selection-mode sync, Paver out-of-plane growth, Paver return-path merge, and Object Snap Undo are implemented as a bugfix candidate. Blender 4.5 regression retest is the immediate gate before additional feature scope or Quickbar exposure.''')

project_state = '''# Witch Tools Project State

Last updated: 2026-08-08

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit and reusable mesh/topology backend
- Development branch: `feature/witch-tools-magic-branch`
- Dev_v2.10.0 tested baseline: `f010eaa136dd8e68b78485858a369d38fc89a078`
- Current candidate: `Dev_v2.10.1`
- Target Blender: `4.5.0`
- Public/release branches modified: no
- Witch Dock / Quickbar modified: no

## Last completed work

Dev_v2.10.0 was user-tested in Blender 4.5. Passing behavior: hover highlighting, Magnetic Snap, Inject New Undo/Redo, Paver, Organic, and tested Organic magnetic vertex merge. The test exposed multi-edge Edge-source, multi-contact merge, stale unsplit target-edge, Magic Branch camera/activation/selection-mode, Paver out-of-plane/return-path merge, and Object Snap Undo failures.

Dev_v2.10.1 source fixes are implemented: Edge Solo/Branch supports one or more selected edges; Auto-Merge scans every created vertex and splits existing target edges before welding interior contacts; MMB pivot changes occur only on plain MMB during a live drag; Magic Branch has explicit ON/OFF plus separate Persistent behavior; Branch Type switches Blender mesh selection mode; Paver can grow out of plane under explicit axis constraints; Object Snap pushes an explicit Undo boundary.

## Current known-working state

The Dev_v2.10.0 behaviors listed above are user-confirmed in Blender 4.5. Dev_v2.10.1 package Python syntax/version validation passed during source patch integration. Do not infer Dev_v2.10.1 runtime success from those static checks.

## Active problems / limitations

Dev_v2.10.1 requires Blender 4.5 retest for multi-edge source behavior, every Auto-Merge topology case, normals/winding/material/custom-edge-data preservation, cancel/Undo/Redo, Magic Branch modal lifecycle and camera navigation, selection-mode Undo restoration, Z-wall Paver dimensions, return-path Paver merge, and Object Snap Undo. Dynamic unselected-fan Slide and arbitrary face-interior retopology remain deferred. Persistent per-branch Undo and Edit Tools drag-grip reordering remain runtime-unverified.

## Next exact implementation step

Install Dev_v2.10.1 in Blender 4.5 and run the regression blocks in the Precision Edit and Magic Branch test plans. Fix only observed failures before starting new feature scope or Witch Dock/Quickbar exposure.

## Files changed

Source: `precision_edit_topology.py`, `precision_edit_drag.py`, `operators_inject_new.py`, `operators_magic_branch.py`, `precision_edit_props.py`, `panel_precision_edit.py`, `operators_object_snap.py`, `operators_ui.py`, `__init__.py`, `state.py`, plus source quick starts/changelog/readme/compatibility. Repository documentation: Precision Edit and Magic Branch packets, UI map, roadmap, project state, notes and compatibility metadata.

## Test status

- Dev_v2.10.0 Blender 4.5 user pass: performed and recorded above
- Dev_v2.10.1 Python AST/version validation: passed
- Dev_v2.10.1 Blender 4.5 runtime: not performed
- Additional Blender versions: not tested
- Public release / Quickbar changes: none
'''
(ROOT/'addons/witch_tools/docs/PROJECT_STATE.md').write_text(project_state, encoding='utf-8')

latest = '''# Witch Tools Notes Changelog — Latest Update

Date: 2026-08-08

## Dev_v2.10.1 — Blender 4.5 runtime-fix documentation

- Recorded Dev_v2.10.0 user runtime results and the exact failing merge/navigation/undo cases.
- Patched canonical Witch Tools Inject New/Magic Branch topology integration, navigation/activation, Paver axis growth, and Object Snap Undo.
- Updated Precision Edit and Magic Branch specs, decisions, states, roadmaps and regression tests.
- Candidate: `Dev_v2.10.1`, target Blender `4.5.0`; runtime retest pending.
'''
(ROOT/'addons/witch_tools/docs/NOTES_CHANGELOG.md').write_text(latest, encoding='utf-8')
prepend_once('addons/witch_tools/docs/NOTES_CHANGELOG_FULL.md', '## Dev_v2.10.1 — Blender 4.5 runtime-fix documentation', latest.replace('# Witch Tools Notes Changelog — Latest Update\n\n',''))

root_latest = '''# Blender.Tools Notes Changelog — Latest Update

## 2026-08-08 — Witch Tools Dev_v2.10.1 runtime fix candidate

- Recorded Blender 4.5 user-test results for Witch Tools Dev_v2.10.0.
- Patched canonical Witch Tools topology integration, Magic Branch interaction behavior, Paver axis growth, and Object Snap Undo.
- Updated Witch Tools project/feature/test documentation and Dev_v2.10.1 packaging metadata.
- Public release branches and Witch Quickbar are unchanged. Runtime retest is pending.
'''
(ROOT/'NOTES_CHANGELOG.md').write_text(root_latest, encoding='utf-8')
prepend_once('NOTES_CHANGELOG_FULL.md', '## 2026-08-08 — Witch Tools Dev_v2.10.1 runtime fix candidate', root_latest.replace('# Blender.Tools Notes Changelog — Latest Update\n\n',''))
prepend_once('Blender_Version_Compatability.md', '## Witch Tools Dev_v2.10.1 — 2026-08-08', '''## Witch Tools Dev_v2.10.1 — 2026-08-08

- Intended Blender target: 4.5.0
- Runtime baseline: Dev_v2.10.0 user-tested in Blender 4.5; merge/navigation/undo defects found
- Dev_v2.10.1 runtime verification: pending
- Additional Blender versions verified for Dev_v2.10.1: none
- Public releases / Quickbar: unchanged''')

workflow = ROOT/'.github/workflows/package-witch-tools-v2-10.yml'
s = workflow.read_text(encoding='utf-8')
s = s.replace('Package Witch Tools Dev v2.10.0','Package Witch Tools Dev v2.10.1')
s = s.replace("'version': (2, 10, 0)", "'version': (2, 10, 1)")
s = s.replace('Dev_v2.10.0 / Blender 4.5','Dev_v2.10.1 / Blender 4.5')
s = s.replace('v2_10_0','v2_10_1')
anchor='          unzip -t Witch_Tools_Dev_v2_10_1_Blender_4_5.zip\n'
manifest='''          cat > Witch_Tools_Dev_v2_10_1_Blender_4_5.manifest.txt <<EOF
          Add-on: Witch Tools
          Version: Dev_v2.10.1
          Target Blender: 4.5.0
          Branch: feature/witch-tools-magic-branch
          Commit: ${GITHUB_SHA}
          Static package validation: Python AST parse + metadata + cache hygiene + ZIP integrity
          Runtime status: Blender 4.5 user retest pending
          EOF
'''
if 'Witch_Tools_Dev_v2_10_1_Blender_4_5.manifest.txt <<EOF' not in s and anchor in s:
    s=s.replace(anchor,anchor+manifest)
upload='            Witch_Tools_Dev_v2_10_1_Blender_4_5.sha256\n'
if 'Witch_Tools_Dev_v2_10_1_Blender_4_5.manifest.txt' not in s.split('Upload package artifact')[-1]:
    s=s.replace(upload,upload+'            Witch_Tools_Dev_v2_10_1_Blender_4_5.manifest.txt\n')
workflow.write_text(s,encoding='utf-8')

for py in sorted(PKG.rglob('*.py')):
    ast.parse(py.read_text(encoding='utf-8'), filename=str(py))
print('Finalized Dev_v2.10.1 docs/packaging; package Python syntax passed.')
