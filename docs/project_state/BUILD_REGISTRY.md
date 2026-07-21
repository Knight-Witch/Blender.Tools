# Blender.Tools Build Registry

This registry records verified baselines. A build is not current merely because it was generated recently or discussed in chat.

## Witch Quickbar

### Public baseline — verified in repository

- Public version: `v1.0.2`
- Internal source correlation: `1.2.8`
- Branch: `Witch_Quick_Access`
- Commit: `13242bf0141c7f539af97b39a4aca6e640c0901c`
- Intended Blender target in metadata: `4.5.0`
- Additional versions tested: not independently verified in this repository audit
- Artifact filename: not yet recorded
- Package folder: not yet recorded
- Update URL: not yet recorded
- Status: public tracked baseline; compatibility branch must remain intact

### Current development baseline

- Version: unknown pending artifact import
- Branch: no dedicated historical dev branch confirmed
- Status: unresolved

## Witch Tools

### Public baseline

- Version: no verified public code baseline found on `Witch_Main_Tools`
- Default branch head: `ed92ded9fde9c1ee812faf227b31383b3eaa674d`
- Branch content state: placeholder documentation only

### Current development baseline

- Expected historical context: a Dev_v2.x line has been developed outside the verified default-branch source
- Exact version: unverified
- Commit: unverified
- Artifact filename: unverified
- Target Blender version: expected `4.5`, must be confirmed from source metadata
- Status: candidate files must be located and imported

## Witch Core

- Current development baseline: not yet imported into this branch
- Target Blender version: expected `4.5`, must be confirmed
- Status: pending audit

## Build-entry requirements

Every future entry must include:

- component
- public or development version
- source branch and commit
- artifact filename
- package folder/add-on identifier
- target Blender version
- additional versions actually tested
- source hash or archive hash
- build date
- test status
- known limitations
- superseded baseline

## Rule

Do not replace an entry marked verified with a remembered or chat-generated version unless the candidate files have been compared and the replacement is explicitly recorded.