# Lab 05: Extraction, filters and dependencies

**Outcome:** explain why extracting one API can include referenced resources.

```bash
python3 scripts/workshop.py extract
python3 scripts/workshop.py extract --no-transitive
python3 scripts/workshop.py extract --full
python3 scripts/workshop.py preview --filter
python3 scripts/workshop.py publish --filter
```

1. Compare `.work/extract-dependencies/` and `.work/extract-exact/`.
2. The API references a backend and policy fragment; the fragment references named values. Dependency expansion includes these when enabled.
3. Inspect `filter.dev-strict.yaml`. It selects the deployed `dev-demo-orders` name. Every unrelated type is explicitly `[]`.
4. Inspect `filter.orders-strict.yaml`. Publishing matches canonical artifact names, so it selects `demo-orders` and explicitly includes the tag needed by the API association.
5. Review the full snapshot in `.work/extract-full/`. It represents the configured service, not a portable production backup guarantee.

**Important:** omitted top-level filter keys mean “include all” for that type. A short `apis: [my-api]` file alone does not constrain the whole extraction to only that API. `--no-transitive` turns off dependency expansion; the destination must already contain required dependencies if you publish that subset.

The complete suite also creates a filter selecting `dev-*` named values while excluding `!dev-demo-release`. It asserts that the environment value is present and the release value is absent. Quotes around exclusions avoid YAML ambiguity. Nested API/workspace filters are documented upstream but not part of the live Consumption exercises.

[Next: Secrets and deletion](06-guards.md)
