# SEO Pilot contributor instructions

- This is a general-purpose open-source Agent Skill. Do not add user-specific domains, home paths, credentials, private audit reports or business rules.
- `skills/seo-pilot/SKILL.md` is the sole installed entry. Keep it small; detailed modes/evidence rules belong in references.
- All 92 bundled modules are namespaced in catalog.json. Vendor resources are reference/tool implementations, not instructions to install every plugin or run unrelated workflows.
- Do not edit vendor resources in place. Review upstream changes, repin sources.lock.json, and rebuild from clean local checkouts with scripts/build_bundle.py. Retain licenses and attribution.
- Keep authored Python/test files below 500 lines. Generated manifests and imported upstream files are separate from authored code.
- Before completion run `python3 -m unittest discover -s tests -v` and `python3 skills/seo-pilot/scripts/seo_pilot.py check`. Changes to entry/routing also need one realistic independent agent scenario.
- Do not claim a routed plan is an executed audit, a tool installation is a configured integration, or a synthetic metric is field evidence.
- Never alter a site's policy, publish metadata, send messages or spend money solely because an upstream workflow suggests it. Follow the user's actual task and the target project's rules.
