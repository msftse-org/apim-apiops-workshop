# Lab 11: Cleanup

**Outcome:** remove your workshop resources after reviewing the target.

```bash
python3 scripts/resources.py list
python3 scripts/resources.py plan
# Replace the argument with the exact resource group in config.local.json.
python3 scripts/resources.py cleanup --delete-resource-group YOUR-WORKSHOP-RESOURCE-GROUP
```

Cleanup deletes the **entire configured resource group**. It requires both the exact group name and a workshop purpose tag. Do not put unrelated resources in that group. The script refuses a mismatched name or missing tag.

The instructor's reference environment stays deployed for demonstrations; whole-group deletion was intentionally not executed during the latest workshop validation. The disposable secret/deletion exercise does clean up its own temporary named value.

For a hosted setup, separately remove the workshop role assignment, Entra app/federated credential and repository variables when you retire that setup. Group deletion alone does not delete tenant-level identities or GitHub configuration.

[Return to workshop](../../README.md)
