# Lab 10: Verify the workshop outcomes

**Outcome:** validate the observable results with native tools.

```bash
curl --fail-with-body -sS -D .work/dev.headers -o .work/dev.body \
  "https://$APIM_NAME.azure-api.net/dev/orders/status"
curl --fail-with-body -sS -D .work/qa.headers -o .work/qa.body \
  "https://$APIM_NAME.azure-api.net/qa/orders/status"
grep -i 'x-demo-' .work/dev.headers .work/qa.headers
jq -e '.status == "ok" and .synthetic == true' .work/dev.body .work/qa.body
grep -qi 'x-demo-environment: dev' .work/dev.headers
grep -qi 'x-demo-release: v1' .work/dev.headers
grep -qi 'x-demo-environment: qa' .work/qa.headers
grep -qi 'x-demo-release: v2' .work/qa.headers
jq -se '.[0].summary.totalExtracted > .[1].summary.totalExtracted' \
  .work/extract-dependencies.json .work/extract-exact.json
jq -e '.summary.totalPuts == 1' "$RELEASE_LAB/change-preview.json"
jq -e '.summary.totalPuts == 0' "$RELEASE_LAB/override-preview.json"
jq -e '.dryRun.actions | length == 1 and .[0].operation == "DELETE" and .[0].type == "NamedValue" and .[0].name == "workshop-temporary"' "$DELETE_LAB/delete-plan.json"
test -f .work/extract-patterns/namedValues/dev-demo-environment/namedValueInformation.json
test ! -f .work/extract-patterns/namedValues/dev-demo-release/namedValueInformation.json
test ! -f "$DELETE_LAB/extracted/namedValues/dev-workshop-temporary/namedValueInformation.json"
test "$(find .work/apic-backup -name 'specification.*' | wc -l | tr -d ' ')" -gt 0
test "$(find .work/apic-metadata -name 'specification.*' | wc -l | tr -d ' ')" -eq 0
test -d "$GITHUB_LAB/.github/prompts"
test -d "$AZDO_LAB/.github/prompts"
echo "All final workshop assertions passed"
```

Check all outcomes:

- Dev is v1 after rollback; QA remains v2. Both return HTTP 200.
- The change preview selected one PUT; the override-only preview selected zero.
- Dependency extraction contains more resources than exact extraction.
- Wildcard extraction includes the environment value and excludes the release value.
- The secret fixture was redacted; unresolved-redaction and filter/delete commands returned 2.
- The deletion plan selected exactly one temporary named value and its stale extracted file disappeared.
- API Center backup includes specifications; metadata-only backup does not.
- Both init platforms generated configuration/prompt files, rejected overwrite with exit 1 and accepted `--force`.

See [recorded validation](../../validation/README.md) for the author's measured run of the same native command blocks. Your tenant, policies, names and permissions may produce different errors.

| Symptom | Check |
|---|---|
| Wrong tenant/subscription | `az account show`, then login/set the intended account |
| Authorization denied | Resource scope and your assigned Azure role |
| Publish fails after dry-run | Inspect the rejected Azure property or dependency |
| Zero incremental changes | Commit parent, artifact paths, ambient `COMMIT_ID` and override-only edits |
| QA name collision | Canonical names in overrides and distinct display names |
| Extra resources extracted | Omitted filter keys include all |
| Old response briefly | Allow gateway propagation and retry |
| Only echo fails | External httpbin availability; check `/status` separately |

[Next: Cleanup](11-cleanup.md)
