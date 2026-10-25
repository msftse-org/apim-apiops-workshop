# Lab 04: Overrides and the incremental trap

**Outcome:** understand canonical names, prefixes, routes and override-only changes.

Compare `configuration.dev.yaml` and `configuration.qa.yaml`. QA uses `namePrefix: qa-`, `apiPathPrefix: qa/`, distinct display names and release value v2. Override entries use canonical names such as `demo-release`, not `qa-demo-release`.

Continue in the disposable Git repository from Lab 03. Add a harmless API description override and commit only that configuration file:

```bash
cd "$RELEASE_LAB"
cat >> configuration.dev.yaml <<'YAML'
apis:
  - name: demo-orders
    properties:
      description: "Environment override workshop exercise"
YAML
git add configuration.dev.yaml
git commit -m "Override-only change"
OVERRIDE_COMMIT=$(git rev-parse HEAD)
apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source apim-artifacts --overrides configuration.dev.yaml --commit-id "$OVERRIDE_COMMIT" --dry-run --format json > override-preview.json
jq '.summary.totalPuts' override-preview.json
```

Expected: **0**. Incremental selection uses artifact changes, so this commit does not select the API. Apply a full publish instead, then restore the original override file:

```bash
apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source apim-artifacts --overrides configuration.dev.yaml
git revert --no-edit "$OVERRIDE_COMMIT"
apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source apim-artifacts --overrides configuration.dev.yaml
cd "$WORKSHOP_ROOT"
```

The full publish sends the artifact set with environment overrides applied. This lab uses a shared gateway for cost control. Separate production environments usually use separate services, backend URLs and secret references.

[Next: Extraction and filters](05-filtering.md)
