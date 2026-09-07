# Scandinavian–Mediterranean design evolution

Date: 2026-09-07
Status: Historical exploration plan. Use `../HANDOFF.md` for current status and remaining work.

The repository contract is implemented in v4.0.1. Website application remains pending.
The steps below mix completed work with exploratory proposals. Do not execute them as an outstanding checklist.

## Design objective

Create a minimal, functional, and elegant system with warmth and human presence.
Use Scandinavian clarity through alignment, useful objects, readable type, and simple controls.
Express Mediterranean warmth through soft neutrals, natural light, comfortable proportions, and approachable language.
Express the direction through clear typography, comfortable spacing, warm neutrals, and approachable language.
Use the companion website brief, `agustos-iskandivvian-website-brief-2026-09-07.md`, to guide visual decisions.

Keywords: calm, warm, functional, elegant, natural, spacious, human, approachable, precise.

Apply this direction across the portfolio. Adjust its intensity to the task.
Editorial pages can carry more atmosphere. Software and technical documents need stronger visual restraint.

## Proposed visual decisions

| Area | Proposed change | Boundary |
|---|---|---|
| Surfaces | Develop warm white, pale limestone, and muted sand surfaces. Compare them with the current cream. | Select final values from rendered examples. Keep white and dark themes functional. |
| Color | Use neutral surfaces to carry warmth. Keep red as a clear interaction signal. | Preserve registered identity inks and semantic status colors. |
| Typography | Retain Inter Tight, Inter, and JetBrains Mono. Test calmer display weights and more comfortable paragraph spacing. | Preserve Inter Tight 650 for wordmarks. Keep technical values legible. |
| Composition | Pair clear alignment with generous openings, varied image sizes, and occasional asymmetric editorial layouts. | Preserve reading order and one shared alignment frame. |
| Photography | Show natural light, real installations, material details, and people using spaces. | Preserve accurate product color, geometry, and technical evidence. |
| Components | Use warm surface groups, selective borders, and modest corners. Reduce unnecessary card containers. | Keep control boundaries, focus, and selected states clear. |
| Motion | Use brief, quiet feedback for actions and state changes. | Preserve reduced-motion behavior. |
| Voice | Use direct language about people, places, materials, and practical benefits. | Preserve factual claims and technical terminology. |

Avoid full-page noise overlays, distressed type, decorative arches, and a separate decorative palette for each brand.
Use olive and clay tones within photography before considering additional interface colors.

## Repository implementation sequence

1. Establish a visual baseline.

   Capture the current UI reference and representative Astro pages at mobile and desktop sizes.
   Include cream, white, dark, forms, tables, and each brand lockup.
   Retain these captures as dated evidence under `artifacts/`.

2. Develop and select the visual direction.

   Compare three treatments: warm clarity, approachable editorial, and sunlit imagery.
   Compare how each treatment uses typography, spacing, and language.
   Use the same Turkish and English content for each treatment.
   Include an editorial opening, Pataraz product section, and compact software form.
   Select one treatment before changing shared production tokens.
   Record exact colors, weights, spacing, image rules, and component treatments from the selected examples.

3. Update the authoritative design rules.

   Update `DESIGN.md` with the new objective, surface roles, photography guidance, and composition examples.
   Clarify that warmth comes from composition, color, and language.
   Append the decision and its reasons to `MEMORY.md`. Preserve earlier entries as historical evidence.
   Update `PATARAZ.md` with material photography and product presentation guidance.
   Update `AGENTS.md` and `README.md` so future contributors find the new rules.
   Correct the README source list: the generated handoff file must not appear under hand-editable sources.

4. Implement foundations and recipes.

   Edit `tokens/design-tokens.json` for selected neutral colors, semantic surfaces, typography values, and recipe settings.
   Add roles only when representative examples demonstrate a repeated need.
   Edit `tokens/web.css.tmpl` for surface application, editorial compositions, and component styling.
   Keep existing public classes and variables compatible where practical.
   Map new surface roles explicitly in white and dark themes.
   Fix faint text contrast where the existing system uses it for readable content.

5. Update generation and distribution.

   Update `scripts/build_design_system.py` to generate new roles and the revised design contract.
   Update `ui/UI-KIT.md.tmpl`, `ui/starter.html.tmpl`, and `ui/AGENTS-SNIPPET.md.tmpl`.
   Update `ui/check-agustos-ui.py.tmpl` where new rules require automated enforcement.
   Extend the reference page with a warm editorial composition and a complete example without imagery.
   Regenerate CSS, resolved tokens, the handoff, the UI kit, adapters, and manifests.
   Never edit generated outputs directly.

6. Translate the direction across media.

   Update Astro reference compositions and any affected Rails partials.
   Verify WordPress token mappings and shared recipes.
   Review `brand/build_templates.py`, `brand/build_presentation.mjs`, and `brand/build_datasheet.py` for affected styling.
   Apply generous spacing and warm surfaces to presentations where appropriate.
   Keep document body pages and technical datasheets plain and economical to print.
   Regenerate affected artifacts for every supported brand using documented build commands.
   Register added material assets and changed brand assets in `ASSETS.md`.
   Store source images with provenance and reuse rights.

7. Verify and release.

   Update relevant contract tests under `tests/` for new semantic roles, theme mappings, and generated output coverage.
   Run the repository checks listed below.
   Inspect rendered web pages, documents, presentations, and affected datasheets.
   Target version 4.0.0 because the repository classifies philosophy shifts as major changes.
   Update `VERSION` and the token registry together, then regenerate versioned outputs.
   Document migration steps and create the matching version tag during release.
   Keep consumer repositories on their pinned version until each adopts and verifies the new kit.

## Acceptance criteria

- The new direction appears in typography, composition, and language as well as background color.
- All five brands share the same visual grammar and retain their registered identity.
- Editorial pages feel warm and approachable. Forms and technical content remain easy to scan.
- Text meets the documented contrast requirements on every supported surface.
- Focus, control boundaries, errors, and selected states remain clear.
- Mobile layouts preserve reading order and avoid horizontal overflow.
- Turkish characters render correctly, and the declared fonts load successfully.
- Pages feel warm, human, and complete through typography, spacing, and language.
- Added images have explicit dimensions and appropriate compression. Decorative assets do not block page interaction.
- Office artifacts remain editable, and printed documents remain legible.
- Generated artifacts match their sources. Consumer projects do not redeclare tokens.

## Required repository checks

```bash
python3 scripts/build_design_system.py
python3 scripts/build_design_system.py --check
python3 scripts/check_office_artifacts.py --check
python3 -m unittest discover -s tests
```

Run affected brand generators before the final checks.
Run the UI compliance checker against a representative consumer after migration.
Measure added image transfer size against the captured baseline and investigate regressions.

## Completion boundary

This plan covers the shared repository, its reference implementations, and generated deliverables.
Live consumer websites require separate adoption changes after release.
The first implementation deliverable is the visual comparison using existing fonts, logos, and representative content.
