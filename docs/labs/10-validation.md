# Lab 10: Validation and troubleshooting

```bash
python3 scripts/validate.py
python3 scripts/workshop.py validate-live
```

The complete live suite writes `.work/validation.json`. `completed: true` means every required assertion completed. Each CLI step records its actual and expected exit code. Two publish rejection scenarios deliberately expect exit code 2. Each init overwrite-conflict scenario expects exit code 1. Raw stdout/stderr stay local under `.work/logs/` and scratch exercise directories.

Review these checkpoints:

- Both environment previews and full publishes succeed.
- dev v1 / dev v2 / dev v1 smoke assertions succeed.
- QA remains v2 through the dev release cycle.
- The echo endpoint reaches the backend.
- Dependency extraction contains more resources than exact extraction.
- Filtered publish succeeds and wildcard exclusion removes the specified named value.
- An override-only commit selects zero PUTs.
- Secret extraction redacts the synthetic value and the placeholder publish is rejected.
- Only the disposable named value is deleted, and stale local artifacts disappear.
- API Center backup contains specifications; metadata-only backup does not.
- Both init platforms generate prompts and configurations, reject accidental overwrites and allow explicit force.

## Common failures

| Symptom | What to inspect |
|---|---|
| Authentication failure | `az account show`, correct tenant/subscription, role scope, credential environment variables |
| Exit 1 during publish | Partial failure details in JSON and stderr; fix the rejected artifact then republish |
| Exit 2 during guards | Expected for the named rejection cases; unexpected elsewhere |
| Zero incremental PUTs | Selected commit, parent history and whether files under the artifact source actually changed |
| QA name collision | Canonical override names plus distinct API/product/tag display names |
| Preview succeeds, publish fails | Azure validates properties and relationships beyond the local plan |
| Smoke test fails briefly | Gateway propagation; the helper retries before failing |
| Echo only fails | Availability of the external httpbin backend; check `/status` separately |
| Unexpected extraction scope | Omitted type keys include all; use explicit empty arrays |

Keep results specific to the tested commit and APIM tier. The repository does not claim every supported resource type or cloud environment was exercised.

[Next: Cleanup](11-cleanup.md)
