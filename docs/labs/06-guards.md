# Lab 06: Secrets, rejection and scoped deletion

**Outcome:** see secret redaction, a blocked publish, an explicit single-resource DELETE and stale local-file removal.

```bash
python3 scripts/workshop.py guards
```

The exercise performs these operations in a disposable Git repository:

1. Publish one named value `dev-workshop-temporary` marked secret. Its value is the synthetic string `WORKSHOP-NOT-A-CREDENTIAL`.
2. Extract only that value using a strict filter.
3. Assert the saved `value` is `*** REDACTED ***`.
4. Try publishing the redacted extraction with `--dry-run`. Expect exit code 2 and no deployment.
5. Try combining `--filter` with `--delete-unmatched`. Expect exit code 2.
6. Delete the synthetic artifact locally and commit that one removal.
7. Preview `--commit-id <exact-sha> --delete-unmatched`. Assert the entire plan is exactly one DELETE of `workshop-temporary`.
8. Execute that same pinned plan.
9. Extract again with `--remove-stale`. Assert the obsolete local artifact is gone.

The script attempts cleanup in a `finally` block. If interrupted externally, inspect the most recent `.work/guards-*` repository and logs before retrying. Do not use a full unmatched cleanup to remove a single exercise resource.

Full `--delete-unmatched` can delete remote resources absent from the source folder. Incremental deletion only targets removals in the selected commit. The workshop intentionally uses the latter.

For real secrets, supply environment-specific Key Vault references or pipeline token substitution. A Key Vault reference also requires APIM identity permissions. Those integrations are documented alternatives, not exercised with real secrets in this workshop. The pinned implementation rejects remaining redaction markers; some upstream prose still describes older skip behavior.

[Next: API Center](07-api-center.md)
