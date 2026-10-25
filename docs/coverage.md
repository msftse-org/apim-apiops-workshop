# Coverage and boundaries

The workshop covers every top-level command family in the pinned CLI: `init`, APIM `extract` / `publish`, and API Center `apic extract` / `apic publish`. It exercises important options through runnable labs rather than claiming to test every combination.

| Capability | Exercise | Validation scope |
|---|---|---|
| Full publish and dry-run JSON | 02 | Live dev and QA |
| OpenAPI and operation policies | 02 | Status and echo operations |
| Backend, fragment and named values | 02/05 | Runtime response and extraction |
| Product and tag association | 02/05 | Publish and extraction |
| Environment prefixes and overrides | 04 | Shared gateway dev/QA |
| Incremental update and rollback | 03 | One PUT change and revert |
| Override-only commit | 04 | Zero selected PUTs |
| Exact filters and dependencies | 05 | Compare extraction and filtered publish |
| Wildcards and exclusions | 05 | Named-value inclusion/exclusion assertions |
| Secret redaction and preflight rejection | 06 | Synthetic secret only |
| Commit-scoped deletion | 06 | Exactly one temporary named value |
| Stale artifact removal | 06 | Removed local file assertion |
| API Center metadata/specifications | 07 | Same-instance backup and replay |
| Workspace selection / no specifications | 07 | API Center default workspace |
| GitHub Actions / Azure DevOps init | 08 | Both scaffolds, conflict and force |
| Copilot prompt generation | 08 | Files present; interactive Copilot not automated |
| Hosted GitHub workflow | 09 | See linked execution results |
| Provisioning and cleanup | 01/11 | Existing sandbox reuse; whole-group deletion not rerun |

## Additional upstream features

APIM workspaces, additional API protocols, revisions/version sets, loggers/diagnostics, gateways, subscriptions, schema/documentation resources and many nested override/filter combinations need dedicated fixtures and, in some cases, a different APIM tier. They are documented upstream but not certified by this Consumption workshop. API Center workspaces are separate from APIM workspaces.

Key Vault references, pipeline secret substitution, Azure DevOps hosted execution, sovereign clouds, service-principal secret authentication and managed identity are documented options. The live local path uses Azure CLI; the GitHub path uses federation when configured. No paid APIM tier or real secret store was provisioned merely to increase the checklist.

## Production considerations

This is a demonstration, not a production reference security architecture. The public mock API has no subscription authentication, the environments share a gateway, and the source is pinned for repeatability. The initial upstream dependency audit reported advisories. Evaluate updates, least-privilege identities, isolated environments, approval gates, secret management and broader regression tests before production adoption.

See [official source links](sources.md) and [recorded results](../validation/README.md).
