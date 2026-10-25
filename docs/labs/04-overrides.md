# Lab 04: Environment overrides

**Outcome:** understand how one artifact set produces distinct dev and QA routes.

1. Compare `configuration.dev.yaml` and `configuration.qa.yaml`.
2. Find `environment.namePrefix` and `apiPathPrefix`. These create names such as `qa-demo-orders` and route `/qa/orders`.
3. Observe that override entries still use canonical names such as `demo-environment`, not `qa-demo-environment`.
4. Find the QA release override `v2`. It stays v2 even when the source named value changes for dev.
5. Find QA display-name overrides for the API, product and tag. The original live tests exposed collisions when these were not distinct.
6. Read the `override-only-preview` output in the latest `.work/release-*/.work/logs/` after `cycle`. Expected: zero PUTs when only the configuration file changes in a commit.
7. To apply an override-only change, run a full `python3 scripts/workshop.py publish --env qa`.

A real production promotion would typically target a separate APIM service and different backend/Key Vault references. This shared-gateway pattern is for the workshop and does not create separate security boundaries.

[Next: Filtering](05-filtering.md)
