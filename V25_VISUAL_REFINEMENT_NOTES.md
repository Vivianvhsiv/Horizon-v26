# Horizon v25 – Visual Refinement Pass

## Change
- Added a bilingual `View one major at a time` selector when the student has selected multiple intended majors.
- The complete network remains visible, while the selected major's own discipline and career pathway is illuminated and other areas are faded.
- Switching the selector changes only the map's visual focus; it does not alter the student's stated major choices or recommendation data.
- Updated bilingual helper text to explain the focused pathway behavior.

## Rationale
The multi-major screenshot showed the selected pathways merging into a dense highlighted cluster. A per-major focus control makes each pathway inspectable without discarding the full-map context.

## Validation
- `python -m py_compile app.py`: passed.
- `python qa_check.py`: 574/574 passed.
- `python qa_v25.py`: 8/8 passed.
- Browser-level interaction and visual regression testing remain outstanding.

## Scope limits
This refinement improves navigation and visual focus. It does not certify the accuracy of academic mappings or university prerequisites. The live Railway deployment is unchanged.
